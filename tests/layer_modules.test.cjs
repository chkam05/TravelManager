const {test}=require('node:test');
const assert=require('node:assert/strict');
const {readFileSync}=require('node:fs');
const vm=require('node:vm');
const deferred=()=>{let resolve,reject;const promise=new Promise((a,b)=>{resolve=a;reject=b});return {promise,resolve,reject}};
const json=data=>({ok:true,json:async()=>data});
function storeHarness(){
    const listeners={},requests=[];
    const document={addEventListener:(name,fn)=>(listeners[name]||=[]).push(fn),dispatchEvent:event=>(listeners[event.type]||[]).forEach(fn=>fn(event))};
    const window={};
    vm.runInNewContext(readFileSync('assets/js/layers/store.js','utf8'),{
        window,document,structuredClone,CustomEvent:class{constructor(type){this.type=type}},
        fetch:(url,options)=>{const response=deferred();requests.push({url,options,...response});return response.promise},
    });
    return {store:window.travelManagerCustomLayers,requests,document};
}

test('parallel readers share one request; each gets an isolated snapshot',async()=>{
    const {store,requests}=storeHarness();const a=store.list(),b=store.list(),c=store.list();
    assert.equal(requests.length,1);requests[0].resolve(json({layers:[{id:'a',elements:[]}]}));
    const [one,two]=await Promise.all([a,b,c]);one[0].elements.push('local edit');
    assert.deepEqual(two[0].elements,[]);assert.deepEqual((await store.list())[0].elements,[]);assert.equal(requests.length,1);
});

test('refresh replaces an in-flight generation and late responses cannot restore old data',async()=>{
    const {store,requests}=storeHarness();const old=store.list();const fresh=store.refresh();
    assert.equal(requests.length,2);requests[1].resolve(json({layers:[{id:'new'}]}));await fresh;
    requests[0].resolve(json({layers:[{id:'old'}]}));assert.equal((await old)[0].id,'new');
    assert.equal((await store.list())[0].id,'new');assert.equal(requests.length,2);
});

test('a stale request failure cannot replace a newer successful result',async()=>{
    const {store,requests}=storeHarness();const old=store.list(),fresh=store.refresh();
    requests[1].resolve(json({layers:[{id:'new'}]}));await fresh;requests[0].reject(Error('old failure'));
    assert.equal((await old)[0].id,'new');
});

test('save, delete and import notifications invalidate the cache',async()=>{
    const {store,requests,document}=storeHarness();let read=store.list();requests.at(-1).resolve(json({layers:[]}));await read;
    const save=store.save({id:'new'});requests.at(-1).resolve(json({layer:{id:'new'}}));await save;
    read=store.list();requests.at(-1).resolve(json({layers:[{id:'new'}]}));await read;
    const remove=store.delete('new');requests.at(-1).resolve(json({status:'ok'}));await remove;
    read=store.list();requests.at(-1).resolve(json({layers:[]}));await read;
    document.dispatchEvent({type:'travel-manager:custom-layers-changed'});
    read=store.list();requests.at(-1).resolve(json({layers:[{id:'imported'}]}));assert.equal((await read)[0].id,'imported');
    assert.equal(requests.filter(r=>!r.options.method).length,4);
});

test('failed reads release the pending request so retry can succeed',async()=>{
    const {store,requests}=storeHarness();const failure=store.list();requests[0].reject(Error('offline'));
    await assert.rejects(failure,/offline/);const retry=store.list();requests[1].resolve(json({layers:[]}));assert.deepEqual(await retry,[]);
});

function geometry(){const window={};vm.runInNewContext(readFileSync('assets/js/layers/geometry.js','utf8'),{window});return window.travelManagerLayerGeometry}

test('splitting a curve preserves its shape and moving a node preserves attached handles',()=>{
    const g=geometry(),element={type:'line',points:[[0,0],[3,3]],segments:[{type:'curve',control1:[0,3],control2:[3,0]}]};
    const before=g.sampled(element.points[0],element.points[1],element.segments[0]);
    g.splitSegment(element,0);
    const left=g.sampled(element.points[0],element.points[1],element.segments[0]);
    const right=g.sampled(element.points[1],element.points[2],element.segments[1]);
    before.forEach((point,i)=>{const after=i<=12?left[i*2]:right[(i-12)*2];assert.ok(Math.hypot(point[0]-after[0],point[1]-after[1])<1e-12)});
    const segment=element.segments[0];const control=[...segment.control1];g.moveNode(element,0,[1,1]);
    assert.equal(element.segments[0],segment);assert.deepEqual([...segment.control1],[control[0]+1,control[1]+1]);
});

test('deleting a triangle vertex converts it to an open line with matching segment count',()=>{
    const g=geometry();const e={type:'area',points:[[0,0],[1,0],[1,1]],segments:[{type:'line'},{type:'line'},{type:'line'}]};
    assert.equal(g.deleteVertex(e,0),true);assert.equal(e.type,'line');assert.equal(e.points.length,2);assert.equal(e.segments.length,1);
    assert.equal(g.deleteVertex(e,0),false);
});

test('map collection ignores a stale render completion and preserves the last drawing on failure',async()=>{
    const pending=[],window={travelManagerCustomLayers:{list:()=>{const d=deferred();pending.push(d);return d.promise}}};
    vm.runInNewContext(readFileSync('assets/js/layers/renderer.js','utf8'),{window});
    let clears=0;const render=window.travelManagerLayerRenderer.createCollection({clearLayers:()=>clears++},{});
    const old=render(),latest=render();pending[1].resolve([]);assert.equal(await latest,true);
    pending[0].resolve([]);assert.equal(await old,false);assert.equal(clears,1);
    const failed=render();pending[2].reject(Error('offline'));assert.equal(await failed,false);assert.equal(clears,1);
});

test('clearing recovery waits for an in-flight write and cannot resurrect a discarded draft',async()=>{
    const calls=[],window={setTimeout:()=>1,clearTimeout(){},travelManagerLayerApi:{request:(url,options)=>{const d=deferred();calls.push({...d,options});return d.promise}}};
    vm.runInNewContext(readFileSync('assets/js/layers/draft.js','utf8'),{window});
    const client=window.travelManagerLayerDraft.create(()=>({version:1}),()=>{});
    const write=client.flush();await new Promise(resolve=>setImmediate(resolve));
    const clear=client.clear();assert.equal(calls.length,1);calls[0].resolve({status:'ok'});await write;
    await new Promise(resolve=>setImmediate(resolve));assert.equal(calls[1].options.method,'DELETE');calls[1].resolve({status:'ok'});await clear;
});
