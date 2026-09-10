// Exercise the real editor event handlers with a small DOM/Leaflet adapter.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const vm = require('node:vm');
const {randomUUID} = require('node:crypto');

class Node {
    constructor(tag = 'div') {
        this.tag = tag; this.children = []; this.dataset = {}; this.attrs = {};
        this.value = ''; this.hidden = false; this.listeners = {};
        const classes = new Set(), styles = new Map();
        this.classList = {add: x => classes.add(x), remove: x => classes.delete(x), contains: x => classes.has(x), toggle: (x, on) => on ? classes.add(x) : classes.delete(x)};
        this.style = {setProperty: (k, v) => styles.set(k, v), getPropertyValue: k => styles.get(k) || ''};
    }
    remove() {}
    append(...nodes) { this.children.push(...nodes); }
    replaceChildren(...nodes) { this.children = nodes; }
    setAttribute(k, v) { this.attrs[k] = v; }
    getAttribute(k) { return this.attrs[k]; }
    addEventListener(name, handler) { (this.listeners[name] ||= []).push(handler); }
    removeEventListener(name,handler) { this.listeners[name]=(this.listeners[name]||[]).filter(item=>item!==handler); }
    closest(selector) { return selector.split(',').includes(this.tag)?this:null; }
    focus() {}
    contains(node) { return node === this || this.children.some(child => child.contains(node)); }
    getBoundingClientRect() { return {left: 0, right: 380, top: 0, bottom: 500, width: 380, height: 500}; }
    querySelector(selector) {
        return this.children.find(child => child.tag === selector) || this.children.map(child => child.querySelector(selector)).find(Boolean) || null;
    }
}
const layerData = () => ({id: 'layer-1', name: 'Test', elements: [{id: 'element-1', name: 'Line', type: 'line', points: [[50,20], [51,21]], width: 4, color: '#123456', segments: [{type:'line'}]}]});
const deferred = () => { let resolve, reject; const promise = new Promise((a,b) => {resolve=a;reject=b}); return {promise,resolve,reject}; };

test('drawing coordinate tooltip shows X and Y only for an active tool', () => {
    const source = readFileSync('assets/js/panels/layer.js', 'utf8');
    const styles = readFileSync('assets/css/panels/layer.css', 'utf8');
    assert.match(source, /coordinateX\.textContent = `X: \$\{point\.lng\.toFixed\(6\)\}`/);
    assert.match(source, /coordinateY\.textContent = `Y: \$\{point\.lat\.toFixed\(6\)\}`/);
    assert.match(source, /if \(!state\.mode \|\| state\.transitioning\)/);
    assert.match(source, /hideCoordinateTooltip\(\);[\s\S]*state\.mode = null|state\.mode = null;[\s\S]*hideCoordinateTooltip\(\)/);
    assert.match(styles, /\.layer-drawing-coordinate-tooltip\{/);
    assert.match(styles, /\.layer-drawing-coordinate-tooltip\[hidden\]\{display:none\}/);
});

test('active drawing uses a pencil cursor and previews the first point', () => {
    const source = readFileSync('assets/js/panels/layer.js', 'utf8');
    const styles = readFileSync('assets/css/panels/layer.css', 'utf8');
    assert.match(source, /setDrawingCursor\(true\)/);
    assert.match(source, /setDrawingCursor\(false\)/);
    assert.match(source, /if \(!state\.drawing\.length\) \{[\s\S]*L\.circleMarker\(event\.latlng/);
    assert.match(source, /fillOpacity: 0\.35/);
    assert.match(styles, /\.leaflet-container\.layer-map--drawing/);
    assert.match(styles, /cursor:url\("data:image\/svg\+xml/);
});

async function editor(storage = new Map(), recovery = null) {
    const panel = new Node(), nodes = new Map(), doc = new Node(), win = new Node(), map = new Node();
    const tools = ['line','curve','route','area','point'].map(draw => {const button = new Node('button');button.dataset.draw=draw;return button});
    const template = readFileSync('templates/panels/layer.html', 'utf8');
    const [sidebarMarkup, toolsMarkup] = template.split('<aside class="layer-tools-panel"');
    const node = selector => {if(!nodes.has(selector))nodes.set(selector,new Node());return nodes.get(selector)};
    const owns = (markup, selector) => markup.includes(selector.slice(1,-1));
    panel.querySelector = selector => owns(sidebarMarkup, selector) ? node(selector) : null;
    panel.querySelectorAll = () => [];
    panel.setAttribute('aria-hidden','true');
    const toolsPanel=new Node();
    toolsPanel.querySelector=selector=>owns(toolsMarkup, selector) ? node(selector) : null;
    toolsPanel.querySelectorAll=()=>tools;
    toolsPanel.setAttribute('aria-hidden','true');toolsPanel.inert=true;
    node('[data-layer-width]').value = '4';
    node('[data-layer-line-style]').value = 'solid';
    const dialog = new Node();
    doc.querySelector = selector => selector === '#layer-panel' ? panel : selector === '#dialog-layer' ? dialog : selector === '#layer-tools-panel' ? toolsPanel : null;
    doc.createElement = tag => new Node(tag);
    doc.dispatchEvent = event => (doc.listeners[event.type] || []).forEach(handler => handler(event));
    let dragEnabled=true;map.dragging = {disable(){dragEnabled=false},enable(){dragEnabled=true},enabled:()=>dragEnabled};
    win.setTimeout=fn=>{win.draftTimer=fn;return 1};win.clearTimeout=()=>{win.draftTimer=null};
    win.innerWidth=1200;
    map.fitCalls=[];map.fitBounds=(points,options)=>map.fitCalls.push({points:structuredClone(points),options});map.getSize=()=>({x:win.innerWidth,y:800});
    map.scale=1000;
    map.latLngToContainerPoint=p=>({x:p.lng*map.scale,y:p.lat*map.scale,distanceTo(q){return Math.hypot(this.x-q.x,this.y-q.y)}});
    map.containerPointToLatLng=([x,y])=>({lat:y/map.scale,lng:x/map.scale});
    map.mouseEventToLatLng=e=>({lat:e.clientY,lng:e.clientX});
    map.distance = (a,b) => Math.hypot(a[0]-b[0],a[1]-b[1])*1000;
    map.on = (name,handler) => map.addEventListener(name,handler);
    map.off = (name,handler) => {map.listeners[name]=(map.listeners[name]||[]).filter(item=>item!==handler)};
    const shapes = [];
    const shape = (points, options) => {
        const value = new Node();value.points=points;value.options=options;
        value.getElement=()=>value;value.addTo=()=>value;value.remove=()=>{};value.on=(name,fn)=>value.addEventListener(name,fn);
        value.setLatLng=()=>value;value.setContent=content=>{value.content=content;return value};value.setLatLngs=()=>value;
        shapes.push(value);return value;
    };
    const latLng = point => ({lat:point[0],lng:point[1],distanceTo:other=>Math.hypot(point[0]-other.lat,point[1]-other.lng)*100000});
    const posts = [], patches = [], prompts = [], saved = new Map();let ui={};
    let postHandler = async data => ({ok:true,json:async()=>({layer:data})});
    win.travelManagerMap={map};win.i18n={locale:'en_US',t:key=>key};
    win.travelManagerDialogs={saveDiscardCancel:async options=>{prompts.push(options);return win.choice||'cancel'}};
    const draftWrites=[];
    const fetch = async (url,options={}) => {
        if(url==='/api/custom-layer-draft'){if(options.method==='PUT'){recovery=JSON.parse(options.body);draftWrites.push(recovery)}else if(options.method==='DELETE'){recovery=null;draftWrites.push(null)}return {ok:true,json:async()=>({draft:recovery})}}
        if(options.method==='PATCH'){const data=JSON.parse(options.body);patches.push(data);ui={...ui,...data};return {ok:true,json:async()=>({ui})}}
        if(options.method==='POST') {const data=JSON.parse(options.body);posts.push(data);const response=await postHandler(data);if(response.ok)saved.set(data.id,data);return response;}
        return {ok:true,json:async()=>url==='/api/settings/ui'?{ui}:{layers:[...saved.values()]}};
    };
    const context = vm.createContext({document:doc,window:win,fetch,crypto:{randomUUID},structuredClone,Intl,console,
        CustomEvent:class {constructor(type,options={}){this.type=type;this.detail=options.detail}},
        getComputedStyle:()=>({getPropertyValue:()=>'',minWidth:'280px',maxWidth:'520px'}),
        localStorage:{getItem:key=>storage.get(key)||null,setItem:(key,value)=>storage.set(key,value)},setTimeout:fn=>fn(),
        L:{layerGroup:shape,polyline:shape,polygon:shape,circleMarker:shape,tooltip:shape,latLng,DomEvent:{stopPropagation(){}}}
    });
    for(const name of ['geometry','renderer','store','editor_state','draft'])vm.runInContext(readFileSync(`assets/js/layers/${name}.js`,'utf8'),context);
    vm.runInContext(readFileSync('assets/js/panels/layer.js','utf8'),context);
    doc.dispatchEvent({type:'travel-manager:views-ready'});
    return {
        panel,toolsPanel,win,posts,patches,prompts,shapes,map,doc,tools,dialog,storage,draftWrites,api:win.travelManagerLayerEditor,
        node,
        key:(key,target=new Node())=>(doc.listeners.keydown||[]).forEach(fn=>fn({key,target,preventDefault(){},stopPropagation(){}})),
        setPost:handler=>{postHandler=handler},
        save:()=>panel.querySelector('[data-layer-save]').onclick(),
        draw:mode=>tools.find(button=>button.dataset.draw===mode).onclick(),
        click:point=>(map.listeners.click||[]).forEach(fn=>fn({latlng:latLng(point)})),
        select:()=>panel.querySelector('[data-layer-elements]').children[0].onclick(),
        setWidth:value=>{const input=node('[data-layer-width]');input.value=value;input.onchange()},
        unsaved:()=>{let prevented=false;(win.listeners.beforeunload||[]).forEach(fn=>fn({preventDefault:()=>{prevented=true}}));return prevented}
    };
}

test('selection remains editable across consecutive saves',async()=>{
    const e=await editor();await e.api.open(layerData());e.select();await e.save();
    e.setWidth(8);await e.save();
    assert.equal(e.posts[1].elements[0].width,8);assert.equal(e.unsaved(),false);
});

test('save commits a route sketch and rejects an incomplete area without losing it',async()=>{
    const e=await editor();await e.api.open();e.draw('route');e.click([50,20]);e.click([51,21]);
    assert.equal(e.unsaved(),true);assert.equal(await e.save(),true);
    assert.equal(e.posts[0].elements[0].points.length,2);assert.equal(e.api.isDrawing(),false);
    e.draw('area');e.click([50,20]);e.click([51,21]);
    assert.equal(await e.save(),false);assert.equal(e.posts.length,1);assert.equal(e.api.isDrawing(),true);
    e.click([50,22]);assert.equal(await e.save(),true);assert.equal(e.posts[1].elements[1].type,'area');
});

test('cancel/discard protects a partial sketch when switching layers',async()=>{
    const e=await editor();await e.api.open();e.draw('route');e.click([50,20]);
    assert.equal(await e.api.open(layerData()),false);assert.equal(e.api.isDrawing(),true);
    e.win.choice='discard';assert.equal(await e.api.open(layerData()),true);
    assert.equal(e.api.isDrawing(),false);assert.equal(e.node('[data-layer-title]').textContent,'Test');
    assert.equal(e.unsaved(),false);assert.equal(e.prompts.length,2);
});

test('save-and-close commits the sketch; failed or invalid save keeps the editor open',async()=>{
    const e=await editor();await e.api.open();e.draw('route');e.click([50,20]);e.win.choice='save';
    assert.equal(await e.api.close(),false);assert.equal(e.panel.getAttribute('aria-hidden'),'false');
    e.click([51,21]);e.setPost(async()=>{throw Error('offline')});
    assert.equal(await e.api.close(),false);assert.equal(e.unsaved(),true);
    e.setPost(async data=>({ok:true,json:async()=>({layer:data})}));
    assert.equal(await e.api.close(),true);assert.equal(e.panel.getAttribute('aria-hidden'),'true');
});

test('duplicate save requests are coalesced and edits during save survive',async()=>{
    const e=await editor();await e.api.open(layerData());e.select();e.setWidth(7);
    const pending=deferred();e.setPost(()=>pending.promise);
    const first=e.save(),second=e.save();assert.equal(e.posts.length,1);
    e.setWidth(9);pending.resolve({ok:true,json:async()=>({layer:e.posts[0]})});
    await Promise.all([first,second]);assert.equal(e.unsaved(),true);
    assert.equal(e.node('[data-layer-status]').textContent,'LAYER_EDITOR.SAVED_WITH_CHANGES');
    e.setPost(async data=>({ok:true,json:async()=>({layer:data})}));await e.save();
    assert.equal(e.posts[1].elements[0].width,9);assert.equal(e.unsaved(),false);
});

test('a failed response can be retried with the same layer ID',async()=>{
    const e=await editor();await e.api.open();e.draw('line');e.click([50,20]);e.click([51,21]);
    e.setPost(async()=>{throw Error('lost response')});assert.equal(await e.save(),false);
    assert.equal(e.node('[data-layer-save]').disabled,false);assert.equal(e.unsaved(),true);
    e.setPost(async data=>({ok:true,json:async()=>({layer:data})}));assert.equal(await e.save(),true);
    assert.equal(e.posts[0].id,e.posts[1].id);
});

test('switching waits for an in-flight save and cannot erase newer edits',async()=>{
    const e=await editor();await e.api.open(layerData());e.select();e.setWidth(7);
    const pending=deferred();e.setPost(()=>pending.promise);const save=e.save();e.setWidth(8);
    const opening=e.api.open({...layerData(),id:'layer-2',name:'Other'});
    pending.resolve({ok:true,json:async()=>({layer:e.posts[0]})});await save;
    assert.equal(await opening,false);assert.equal(e.node('[data-layer-title]').textContent,'Test');
    assert.equal(e.unsaved(),true);
});

test('reopening the same layer after save-and-leave does not restore a stale list entry',async()=>{
    const e=await editor(),original=layerData();await e.api.open(original);e.select();e.setWidth(12);
    e.win.choice='save';assert.equal(await e.api.open(original),true);await e.save();
    assert.equal(e.posts.at(-1).elements[0].width,12);
    e.select();e.setWidth(15);e.win.choice='discard';await e.api.open(original);await e.save();
    assert.equal(e.posts.at(-1).elements[0].width,12);
});

test('saving includes an unconfirmed inline element name',async()=>{
    const e=await editor();await e.api.open(layerData());
    const row=e.node('[data-layer-elements]').children[0];
    row.children.at(-1).onclick({stopPropagation(){}});
    e.node('[data-element-menu-rename]').onclick();
    e.node('[data-layer-elements]').querySelector('input').value='Renamed';
    assert.equal(e.unsaved(),true);await e.save();
    assert.equal(e.posts[0].elements[0].name,'Renamed');
});

test('shared confirmation dialog distinguishes save, discard and cancel without changing yes/no results',async()=>{
    const doc=new Node(),win=new Node(),elements=new Map(),buttons=new Map();
    for(const selector of ['#dialog-layer','#yesno-dialog','#yesno-dialog-title','#yesno-dialog-description','#yesno-dialog-icon'])elements.set(selector,new Node());
    for(const result of ['yes','no','cancel'])buttons.set(`[data-dialog-result="${result}"]`,new Node('button'));
    elements.get('#yesno-dialog').querySelector=selector=>buttons.get(selector);
    doc.querySelector=selector=>elements.get(selector);
    doc.createElement=tag=>new Node(tag);
    win.i18n={t:key=>key};win.requestAnimationFrame=fn=>fn();
    vm.runInNewContext(readFileSync('assets/js/dialogs/yesno_dialog.js','utf8'),{document:doc,window:win});
    doc.listeners['travel-manager:views-ready'][0]();
    const click=result=>buttons.get(`[data-dialog-result="${result}"]`).listeners.click[0]();
    for(const [button,result] of [['yes','save'],['no','discard'],['cancel','cancel']]){
        const answer=win.travelManagerDialogs.saveDiscardCancel({});click(button);assert.equal(await answer,result);
    }
    let stopped=false;
    const cancelled=win.travelManagerDialogs.saveDiscardCancel({});
    doc.listeners.keydown[0]({key:'Escape',preventDefault(){},stopImmediatePropagation(){stopped=true}});
    assert.equal(await cancelled,'cancel');assert.equal(stopped,true);
    const information=win.travelManagerDialogs.yesNo({information:true,yesLabel:'Close'});
    assert.equal(buttons.get('[data-dialog-result="no"]').hidden,true);
    click('yes');await information;
    const ordinary=win.travelManagerDialogs.yesNo({});
    assert.equal(buttons.get('[data-dialog-result="no"]').hidden,false);
    assert.equal(buttons.get('[data-dialog-result="cancel"]').hidden,true);
    click('yes');assert.equal(await ordinary,true);
    const selected=win.travelManagerDialogs.choose({choices:[['json','JSON'],['gpx','GPX']]});
    elements.get('#yesno-dialog-description').children.at(-1).value='gpx';click('yes');assert.equal(await selected,'gpx');
    const dismissed=win.travelManagerDialogs.choose({choices:[['json','JSON']]});click('no');assert.equal(await dismissed,null);

});

const shapeData=(type='route')=>{const data=layerData();data.elements[0].type=type;data.elements[0].points=[[50,20],[51,21],[50,22]];data.elements[0].segments=Array.from({length:type==='area'?3:2},()=>({type:'line'}));return data};
const markers=e=>e.shapes.filter(s=>s.options?.radius===6||s.options?.radius===8);
const selectVertex=(e,index,count=3)=>markers(e).slice(-count)[index].listeners.click[0]({latlng:{lat:0,lng:0}});
const event=(overrides={})=>({button:0,isPrimary:true,pointerId:1,clientX:20,clientY:50,preventDefault(){},stopPropagation(){},...overrides});
const emit=(target,name,value)=>[...(target.listeners[name]||[])].forEach(fn=>fn(value));

test('drawing tools obey the same selection rules in UI and action handlers',async()=>{
    for(const [type,index,expected] of [['area',0,[]],['route',1,[]],['route',0,['line','curve','route']],['route',2,['line','curve','route']]]){
        const e=await editor();await e.api.open(shapeData(type));selectVertex(e,index);
        assert.deepEqual(e.tools.filter(t=>!t.disabled).map(t=>t.dataset.draw),expected);
        e.draw('area');assert.equal(e.api.isDrawing(),false);
    }
    for(const type of ['area','route']){
        const e=await editor();await e.api.open(shapeData(type));
        e.shapes.filter(s=>s.options?.opacity===.001).at(-1).listeners.click[0]({});
        assert.ok(e.tools.every(t=>t.disabled));e.draw('line');assert.equal(e.api.isDrawing(),false);
        e.key('Escape');assert.ok(e.tools.every(t=>!t.disabled));
    }
});

test('continuation closes the same shape from either end with line, curve or route',async()=>{
    for(const index of [0,2])for(const tool of ['line','curve','route']){
        const e=await editor();await e.api.open(shapeData());selectVertex(e,index);e.draw(tool);
        const opposite=index===0?[50,22]:[50,20];e.click(opposite);await e.save();
        const elements=e.posts[0].elements;assert.equal(elements.length,1);const shape=elements[0];
        assert.equal(shape.id,'element-1');assert.equal(shape.type,'area');assert.equal(shape.points.length,3);assert.equal(shape.segments.length,3);
        if(tool==='curve')assert.equal(shape.segments.filter(s=>s.type==='curve').length,1);
        assert.equal(new Set(shape.points.map(p=>p.join(','))).size,3);
    }
});

test('area closure uses screen pixels and does not append the closing click',async()=>{
    for(const scale of [1000,10000]){
        const e=await editor();await e.api.open();e.map.scale=scale;e.draw('area');
        e.click([50,20]);e.click([51,21]);e.click([50,22]);e.click([50,20+10/scale]);
        assert.equal(e.api.isDrawing(),false);await e.save();assert.equal(e.posts[0].elements[0].points.length,3);
    }
});

test('Escape cancels, Backspace removes the last point and Enter commits; inputs and dialogs keep their keys',async()=>{
    const e=await editor();await e.api.open();e.draw('route');e.click([50,20]);e.click([51,21]);
    e.key('Escape',new Node('input'));assert.equal(e.api.isDrawing(),true);
    e.dialog.classList.add('dialog-layer--open');e.key('Escape');assert.equal(e.api.isDrawing(),true);e.dialog.classList.remove('dialog-layer--open');
    e.key('Backspace');e.click([52,22]);e.key('Enter');await e.save();
    assert.deepEqual(e.posts[0].elements[0].points,[[50,20],[52,22]]);
    e.draw('area');e.click([40,20]);e.click([41,21]);e.key('Escape');await e.save();assert.equal(e.posts[1].elements.length,1);
});

test('pointer drag completes outside the map and pointer cancellation restores geometry',async()=>{
    const e=await editor();await e.api.open(shapeData());
    const marker=markers(e).slice(-3)[0];emit(marker,'pointerdown',event());assert.equal(e.map.dragging.enabled(),false);
    emit(e.doc,'pointermove',event({clientY:49}));emit(e.doc,'pointerup',event({clientY:49}));
    assert.equal(e.map.dragging.enabled(),true);assert.equal(e.doc.listeners.pointermove.length,0);
    await e.save();assert.deepEqual(e.posts[0].elements[0].points[0],[49,20]);
    const current=markers(e).slice(-3)[0];emit(current,'pointerdown',event());emit(e.doc,'pointermove',event({clientY:48}));emit(e.doc,'pointercancel',event());
    assert.equal(e.map.dragging.enabled(),true);await e.save();assert.deepEqual(e.posts[1].elements[0].points[0],[49,20]);
});

test('panel width is patched, restored and clamped without losing the preferred width',async()=>{
    const e=await editor();await e.api.open();const grabber=e.node('[data-layer-panel-grabber]');
    emit(grabber,'pointerdown',event({clientX:500}));emit(e.doc,'pointermove',event({clientX:300}));emit(e.doc,'pointerup',event());
    await new Promise(resolve=>setImmediate(resolve));assert.equal(e.patches[0].layer_editor_panel_width,580);
    assert.equal(e.toolsPanel.style.getPropertyValue('--layer-sidebar-width'),'580px');
    await e.api.close();await e.api.open();assert.equal(e.panel.style.getPropertyValue('--layer-panel-width'),'580px');
    e.win.innerWidth=400;emit(e.win,'resize',{});assert.equal(e.panel.style.getPropertyValue('--layer-panel-width'),'384px');
    e.win.innerWidth=1200;emit(e.win,'resize',{});assert.equal(e.panel.style.getPropertyValue('--layer-panel-width'),'580px');
});

test('line metrics omit area, area metrics use perimeter and renaming refreshes the map label',async()=>{
    const e=await editor();const data=shapeData();data.show_title=true;await e.api.open(data);
    let row=e.node('[data-layer-elements]').children[0];assert.equal(row.children[2].children.length,1);
    row.children.at(-1).onclick({stopPropagation(){}});e.node('[data-element-menu-rename]').onclick();
    const list=e.node('[data-layer-elements]');list.querySelector('input').value='Updated';list.children[0].children[0].children[1].onclick();
    assert.equal(e.shapes.filter(s=>s.content).at(-1).content.textContent,'Updated');
    e.select();e.node('[data-layer-close-curve]').onclick();e.key('Escape');row=list.children[0];
    assert.equal(row.children[2].children.length,2);assert.equal(row.children[2].children[0].textContent,'LAYER_EDITOR.PERIMETER_VALUE');
});

test('layer list reports fetch errors and retry restores results',async()=>{
    const doc=new Node(),elements=new Map(),win={addEventListener(){},i18n:{locale:'en_US',t:key=>key}};
    const selectors=['#layers-search','#layers-search-input','#layers-sort-button','#layers-sort-menu','[data-layers-list]'];
    selectors.forEach(selector=>elements.set(selector,new Node()));
    doc.querySelector=selector=>elements.get(selector)||null;doc.createElement=tag=>new Node(tag);doc.dispatchEvent=()=>{};
    let offline=true;
    win.travelManagerCustomLayers={list:async()=>{if(offline)throw Error('offline');return []},refresh:async()=>{await doc.listeners['travel-manager:custom-layers-changed'][0]()}};
    vm.runInNewContext(readFileSync('assets/js/views/layers.js','utf8'),{document:doc,window:win,CustomEvent:class{}});
    doc.listeners['travel-manager:views-ready'][0]();await new Promise(resolve=>setImmediate(resolve));
    const list=elements.get('[data-layers-list]');assert.equal(list.children[0].textContent,'LAYER_EDITOR.LOAD_FAILED');
    offline=false;await list.children[1].onclick();assert.equal(list.children[0].textContent,'LAYERS_VIEW.EMPTY');
});

test('curve handle dragging and cancellation restore map dragging and control points',async()=>{
    const e=await editor(),data=layerData();data.elements[0].segments=[{type:'curve',control1:[50.1,20.1],control2:[50.9,20.9]}];
    await e.api.open(data);e.shapes.filter(s=>s.options?.opacity===.001).at(-1).listeners.click[0]({});
    const handle=e.shapes.filter(s=>s.options?.radius===7).at(-2);emit(handle,'pointerdown',event());
    emit(e.doc,'pointermove',event({clientY:50.2,clientX:20.2}));emit(e.doc,'pointerup',event());await e.save();
    assert.deepEqual(e.posts[0].elements[0].segments[0].control1,[50.2,20.2]);
    const next=e.shapes.filter(s=>s.options?.radius===7).at(-2);emit(next,'pointerdown',event());
    emit(e.doc,'pointermove',event({clientY:49,clientX:19}));emit(e.win,'blur',{});await e.save();
    assert.deepEqual(e.posts[1].elements[0].segments[0].control1,[50.2,20.2]);assert.equal(e.map.dragging.enabled(),true);
});

test('dragging updates existing visuals without allocating new Leaflet objects',async()=>{
    const e=await editor(),data=shapeData();
    for(let i=1;i<20;i++)data.elements.push({...structuredClone(data.elements[0]),id:`element-${i+1}`});
    await e.api.open(data);
    const first=markers(e).slice(-60)[0];emit(first,'pointerdown',event());const count=e.shapes.length;
    for(let i=1;i<=20;i++)emit(e.doc,'pointermove',event({clientY:50-i/100}));
    assert.equal(e.shapes.slice(count).filter(shape=>shape.options?.radius!==10).length,0);emit(e.doc,'pointerup',event());await e.save();
    assert.deepEqual(e.posts[0].elements[0].points[0],[49.8,20]);assert.deepEqual(e.posts[0].elements[1].points[0],[50,20]);
});

test('successive curve handle moves all reach the saved geometry',async()=>{
    const e=await editor(),data=layerData();data.elements[0].segments=[{type:'curve',control1:[50.1,20.1],control2:[50.9,20.9]}];
    await e.api.open(data);e.shapes.filter(s=>s.options?.opacity===.001).at(-1).listeners.click[0]({});
    const handle=e.shapes.filter(s=>s.options?.radius===7).at(-2);emit(handle,'pointerdown',event());const count=e.shapes.length;
    for(const value of [50.2,50.3,50.4])emit(e.doc,'pointermove',event({clientY:value,clientX:20.2}));
    assert.equal(e.shapes.slice(count).filter(shape=>shape.options?.radius!==10).length,0);emit(e.doc,'pointerup',event());await e.save();
    assert.deepEqual(e.posts[0].elements[0].segments[0].control1,[50.4,20.2]);
});

test('undo and redo restore style and saved-state detection; new edits clear redo',async()=>{
    const e=await editor();await e.api.open(layerData());e.select();e.setWidth(8);
    const undo=e.node('[data-layer-undo]'),redo=e.node('[data-layer-redo]');
    assert.equal(undo.disabled,false);undo.onclick();assert.equal(e.unsaved(),false);assert.equal(redo.disabled,false);
    redo.onclick();await e.save();assert.equal(e.posts.at(-1).elements[0].width,8);
    undo.onclick();assert.equal(e.unsaved(),true);redo.onclick();assert.equal(e.unsaved(),false);
    undo.onclick();e.setWidth(10);assert.equal(redo.disabled,true);await e.save();assert.equal(e.posts.at(-1).elements[0].width,10);
});

test('drawing and deleting a shape are individually undoable',async()=>{
    const e=await editor();await e.api.open();e.draw('line');e.click([50,20]);e.click([51,21]);
    const undo=e.node('[data-layer-undo]'),redo=e.node('[data-layer-redo]');
    undo.onclick();assert.equal(e.node('[data-layer-elements]').children.length,0);redo.onclick();
    const row=e.node('[data-layer-elements]').children[0];row.children.at(-1).onclick({stopPropagation(){}});
    e.node('[data-element-menu-delete]').onclick();assert.equal(e.node('[data-layer-elements]').children.length,0);
    undo.onclick();assert.equal(e.node('[data-layer-elements]').children.length,1);await e.save();assert.equal(e.posts.at(-1).elements.length,1);
});

test('multiple pointer moves create one undo step and cancelled drags create none',async()=>{
    const e=await editor();await e.api.open(shapeData());const undo=e.node('[data-layer-undo]');
    emit(markers(e).slice(-3)[0],'pointerdown',event());
    for(const y of [49,48,47])emit(e.doc,'pointermove',event({clientY:y}));
    assert.equal(undo.disabled,true);emit(e.doc,'pointerup',event());assert.equal(undo.disabled,false);
    undo.onclick();assert.equal(undo.disabled,true);await e.save();assert.deepEqual(e.posts.at(-1).elements[0].points[0],[50,20]);
    emit(markers(e).slice(-3)[0],'pointerdown',event());emit(e.doc,'pointermove',event({clientY:46}));emit(e.doc,'pointercancel',event());
    assert.equal(undo.disabled,true);
});

test('history is blocked during save and is reset on switching layers',async()=>{
    const e=await editor();await e.api.open(layerData());e.select();e.setWidth(8);
    const pending=deferred();e.setPost(()=>pending.promise);const save=e.save();
    const undo=e.node('[data-layer-undo]');assert.equal(undo.disabled,true);undo.onclick();
    pending.resolve({ok:true,json:async()=>({layer:e.posts[0]})});await save;
    assert.equal(e.unsaved(),false);assert.equal(undo.disabled,false);
    await e.api.open({...layerData(),id:'other'});assert.equal(undo.disabled,true);assert.equal(e.node('[data-layer-redo]').disabled,true);
});

test('history shortcuts leave text inputs and dialogs alone',async()=>{
    const e=await editor();await e.api.open(layerData());e.select();e.setWidth(8);
    const key=(key,extra={})=>emit(e.doc,'keydown',{key,target:new Node(),ctrlKey:true,preventDefault(){},...extra});
    key('z',{target:new Node('input')});assert.equal(e.unsaved(),true);
    e.dialog.classList.add('dialog-layer--open');key('z');assert.equal(e.unsaved(),true);e.dialog.classList.remove('dialog-layer--open');
    key('z');assert.equal(e.unsaved(),false);key('z',{shiftKey:true});assert.equal(e.unsaved(),true);
    key('z',{ctrlKey:false,metaKey:true});assert.equal(e.unsaved(),false);key('y');assert.equal(e.unsaved(),true);
});

test('show on map fits the entire layer or just the chosen shape without editing it',async()=>{
    const e=await editor(),data=layerData();data.elements.push({...structuredClone(data.elements[0]),id:'far',points:[[10,10],[11,11]]});
    await e.api.open(data);assert.equal(e.map.fitCalls.length,1);
    e.node('[data-layer-fit]').onclick();assert.ok(e.map.fitCalls.at(-1).points.some(p=>p[0]===10));
    const row=e.node('[data-layer-elements]').children[0];row.children.at(-1).onclick({stopPropagation(){}});
    e.node('[data-element-menu-fit]').onclick();const call=e.map.fitCalls.at(-1);
    assert.ok(call.points.every(p=>p[0]>=50));assert.equal(call.options.maxZoom,16);
    assert.ok(call.options.paddingBottomRight[0]>24);assert.equal(e.unsaved(),false);
    assert.equal(e.node('[data-layer-undo]').disabled,true);
});

test('show on map includes the sampled curve, not only its endpoints',async()=>{
    const e=await editor(),data=layerData();data.elements[0].points=[[50,20],[50,22]];
    data.elements[0].segments=[{type:'curve',control1:[54,20],control2:[54,22]}];
    await e.api.open(data);const points=e.map.fitCalls[0].points;
    assert.equal(points.length,25);assert.ok(Math.max(...points.map(p=>p[0]))>52);
});

test('empty layers do not move the map and active drawing keeps its viewport',async()=>{
    const e=await editor();await e.api.open();assert.equal(e.node('[data-layer-fit]').disabled,true);
    e.node('[data-layer-fit]').onclick();assert.equal(e.map.fitCalls.length,0);
    await e.api.open(layerData());const before=e.map.fitCalls.length;
    e.draw('route');e.node('[data-layer-fit]').onclick();assert.equal(e.map.fitCalls.length,before);
});

test('recovery restores a partial drawing and allows saving it after completion',async()=>{
    const draft={version:1,layer:{...layerData(),elements:[]},baseline:{...layerData(),elements:[]},mode:'route',drawing:[[50,20]],continuationId:null,continuationVertex:null,style:{width:7,color:'#112233',line_style:'dashed'}};
    const e=await editor(new Map(),draft);e.win.choice='save';await e.api.open();
    assert.equal(e.api.isDrawing(),true);assert.equal(e.unsaved(),true);assert.equal(e.posts.length,0);
    e.click([51,21]);await e.save();assert.deepEqual(e.posts[0].elements[0].points,[[50,20],[51,21]]);
    assert.equal(e.posts[0].elements[0].width,7);await e.api.close();assert.equal(e.draftWrites.at(-1),null);
});

test('recovery can be cancelled without deleting it, or explicitly discarded',async()=>{
    const draft={version:1,layer:layerData(),baseline:layerData(),mode:null,drawing:[],style:{}};
    const e=await editor(new Map(),draft);assert.equal(await e.api.open(),false);assert.equal(e.draftWrites.length,0);
    e.win.choice='discard';assert.equal(await e.api.open(),true);assert.equal(e.draftWrites[0],null);assert.equal(e.unsaved(),false);
});

test('autosave captures an unconfirmed name and the current sketch',async()=>{
    const e=await editor();await e.api.open(layerData());const row=e.node('[data-layer-elements]').children[0];
    row.children.at(-1).onclick({stopPropagation(){}});e.node('[data-element-menu-rename]').onclick();
    e.node('[data-layer-elements]').querySelector('input').value='Recovered name';emit(e.panel,'input',{});
    e.win.draftTimer();await new Promise(resolve=>setImmediate(resolve));
    assert.equal(e.draftWrites.at(-1).layer.elements[0].name,'Recovered name');
    assert.equal(e.posts.length,0);
});


test('separate tools panel follows editor lifecycle and owns drawing controls', async()=>{
    const e=await editor();
    assert.equal(e.panel.querySelector('[data-layer-width]'),null);
    assert.equal(e.toolsPanel.querySelector('[data-layer-save]'),null);
    await e.api.open(layerData());
    assert.equal(e.toolsPanel.classList.contains('is-open'),true);
    assert.equal(e.toolsPanel.getAttribute('aria-hidden'),'false');
    assert.equal(e.toolsPanel.inert,false);
    e.select();e.setWidth(9);emit(e.toolsPanel,'input',{});
    assert.equal(typeof e.win.draftTimer,'function');
    await e.api.close();
    assert.equal(e.panel.classList.contains('is-open'),true);
    assert.equal(e.toolsPanel.classList.contains('is-open'),true);
    assert.equal(e.toolsPanel.inert,false);
    e.win.choice='discard';await e.api.close();
    assert.equal(e.panel.classList.contains('is-open'),false);
    assert.equal(e.toolsPanel.classList.contains('is-open'),false);
    assert.equal(e.toolsPanel.getAttribute('aria-hidden'),'true');
    assert.equal(e.toolsPanel.inert,true);
});


test('point coordinates map X/Y correctly, validate, move curve handles and support undo',async()=>{
    const e=await editor();const data=layerData();
    data.elements[0].segments=[{type:'curve',control1:[50.2,20.2],control2:[50.8,20.8]}];
    await e.api.open(data);e.select();
    const list=e.node('[data-layer-elements]');
    const x=list.children[1].children[1].children[1];
    const y=list.children[1].children[2].children[1];
    assert.equal(x.value,'20');assert.equal(y.value,'50');
    x.onfocus();assert.equal(e.tools.find(b=>b.dataset.draw==='line').disabled,false);
    x.value='181';x.onchange();assert.equal(x.value,'20');assert.equal(e.unsaved(),false);
    y.value='';y.onchange();assert.equal(y.value,'50');
    x.value='22';x.onchange();await e.save();
    assert.deepEqual(e.posts[0].elements[0].points[0],[50,22]);
    assert.deepEqual(e.posts[0].elements[0].segments[0].control1,[50.2,22.2]);
    assert.deepEqual(e.posts[0].elements[0].segments[0].control2,[50.8,20.8]);
    e.node('[data-layer-undo]').onclick();await e.save();
    assert.deepEqual(e.posts[1].elements[0].points[0],[50,20]);
    const current=list.children[1].children[1].children[1];current.value='23';
    current.onkeydown({key:'Escape',preventDefault(){},stopPropagation(){}});
    assert.equal(current.value,'20');assert.equal(e.node('[data-layer-back]').hidden,false);
    e.key('Escape');assert.equal(list.children.length,1);
    e.select();e.node('[data-layer-back]').onclick();assert.equal(list.children.length,1);
});


test('duplicating a layer creates an unsaved isolated copy with fresh IDs',async()=>{
    const e=await editor(),source=layerData();
    await e.api.duplicate(source);
    assert.equal(e.unsaved(),true);assert.equal(e.posts.length,0);
    e.select();e.setWidth(9);await e.save();
    const copy=e.posts[0];
    assert.notEqual(copy.id,source.id);
    assert.notEqual(copy.elements[0].id,source.elements[0].id);
    assert.deepEqual(copy.elements[0].points,source.elements[0].points);
    assert.equal(source.elements[0].width,4);
    assert.equal(copy.elements[0].width,9);
    assert.equal(e.unsaved(),false);
    await e.save();assert.equal(e.posts[1].id,copy.id);
});

test('duplicating a shape preserves geometry and style and is one undoable edit',async()=>{
    const e=await editor(),source=layerData();await e.api.open(source);
    e.node('[data-layer-elements]').children[0].children.at(-1).onclick({stopPropagation(){}});
    e.node('[data-element-menu-duplicate]').onclick();
    await e.save();const [original,copy]=e.posts[0].elements;
    assert.notEqual(original.id,copy.id);
    assert.deepEqual(original.points,copy.points);assert.equal(original.color,copy.color);
    e.node('[data-layer-undo]').onclick();await e.save();assert.equal(e.posts[1].elements.length,1);
    e.node('[data-layer-redo]').onclick();await e.save();assert.equal(e.posts[2].elements[1].id,copy.id);
    e.select();const x=e.node('[data-layer-elements]').children[1].children[1].children[1];
    x.value='25';x.onchange();await e.save();
    assert.equal(e.posts[3].elements[1].points[0][1],20);
});


test('hidden and locked shapes retain list access, resist editing and support undo',async()=>{
    const e=await editor();await e.api.open(layerData());
    const menu=()=>e.node('[data-layer-elements]').children[0].children.at(-1).onclick({stopPropagation(){}});
    menu();e.node('[data-element-menu-locked]').onclick();
    e.select();assert.equal(e.node('[data-layer-elements]').children.length,1);
    menu();assert.equal(e.node('[data-element-menu-delete]').disabled,true);
    e.node('[data-element-menu-delete]').onclick();await e.save();
    assert.equal(e.posts[0].elements.length,1);assert.equal(e.posts[0].elements[0].locked,true);
    const count=e.shapes.length;
    menu();e.node('[data-element-menu-hidden]').onclick();
    // Group allocation is allowed; no shape with point geometry should be created.
    assert.equal(e.shapes.slice(count).some(shape=>Array.isArray(shape.points)),false);
    await e.save();assert.equal(e.posts[1].elements[0].hidden,true);
    e.node('[data-layer-undo]').onclick();await e.save();assert.equal(Boolean(e.posts[2].elements[0].hidden),false);
    menu();e.node('[data-element-menu-locked]').onclick();e.select();
    assert.equal(e.node('[data-layer-back]').hidden,false);
});


test('drawing snaps to vertices and segment interiors, while Alt bypasses snapping',async()=>{
    const e=await editor();await e.api.open(layerData());
    e.draw('line');e.click([50.005,20.005]);
    e.click([52,22]);await e.save();
    assert.deepEqual(e.posts[0].elements[1].points[0],[50,20]);
    e.draw('line');e.click([50.504,20.496]);e.click([53,23]);await e.save();
    assert.deepEqual(e.posts[1].elements[2].points[0],[50.5,20.5]);
    e.draw('line');
    emit(e.map,'click',{latlng:{lat:50.006,lng:20.006},originalEvent:{altKey:true}});
    e.click([54,24]);await e.save();
    assert.deepEqual(e.posts[2].elements[3].points[0],[50.006,20.006]);
});

test('dragging snaps to locked targets but ignores hidden targets and the dragged shape',async()=>{
    const e=await editor(),data=layerData();
    data.elements.push({...structuredClone(data.elements[0]),id:'target',locked:true,points:[[49,19],[48,18]]});
    await e.api.open(data);
    const marker=markers(e).find(s=>s.options.radius!==10);
    emit(marker,'pointerdown',event());emit(e.doc,'pointermove',event({clientY:49.005,clientX:19.005}));
    emit(e.doc,'pointerup',event());await e.save();
    assert.deepEqual(e.posts[0].elements[0].points[0],[49,19]);
    data.elements[1].hidden=true;data.id='hidden-target-layer';await e.api.open(data);
    e.draw('line');e.click([49.005,19.005]);e.click([47,17]);await e.save();
    assert.deepEqual(e.posts[1].elements[2].points[0],[49.005,19.005]);
});


test('curve snapping follows the sampled curve rather than its endpoint chord',async()=>{
    const e=await editor(),data=layerData();
    data.elements[0].points=[[50,20],[50,22]];
    data.elements[0].segments=[{type:'curve',control1:[52,20],control2:[52,22]}];
    await e.api.open(data);e.draw('line');e.click([51.505,21]);e.click([54,24]);await e.save();
    assert.deepEqual(e.posts[0].elements[1].points[0],[51.5,21]);
});

test('Shift dragging translates a whole curve in one undo step and Escape restores it',async()=>{
    const e=await editor(),data=layerData();
    data.elements[0].segments=[{type:'curve',control1:[50.2,20.2],control2:[50.8,20.8]}];
    await e.api.open(data);
    const hit=()=>e.shapes.filter(s=>s.options?.opacity===.001).at(-1);
    emit(hit(),'pointerdown',event({clientY:50,clientX:20}));
    assert.equal(e.map.dragging.enabled(),true);
    emit(hit(),'pointerdown',event({shiftKey:true,clientY:50,clientX:20}));
    emit(e.doc,'pointermove',event({clientY:51,clientX:22}));
    emit(e.doc,'pointermove',event({clientY:52,clientX:23}));
    emit(e.doc,'pointerup',event());await e.save();
    assert.deepEqual(e.posts[0].elements[0].points,[[52,23],[53,24]]);
    assert.deepEqual(e.posts[0].elements[0].segments[0],{type:'curve',control1:[52.2,23.2],control2:[52.8,23.8]});
    e.node('[data-layer-undo]').onclick();await e.save();
    assert.deepEqual(e.posts[1].elements[0].points,data.elements[0].points);
    e.node('[data-layer-redo]').onclick();await e.save();
    emit(hit(),'pointerdown',event({shiftKey:true,clientY:52,clientX:23}));
    emit(e.doc,'pointermove',event({clientY:54,clientX:25}));e.key('Escape');
    assert.equal(e.map.dragging.enabled(),true);assert.equal(e.unsaved(),false);
    await e.save();assert.deepEqual(e.posts[3].elements[0],e.posts[2].elements[0]);
});

test('whole-shape movement rejects out-of-range points without clipping geometry',async()=>{
    const e=await editor();await e.api.open(layerData());
    const hit=e.shapes.filter(s=>s.options?.opacity===.001).at(-1);
    emit(hit,'pointerdown',event({shiftKey:true,clientY:50,clientX:20}));
    emit(e.doc,'pointermove',event({clientY:90,clientX:20}));
    emit(e.doc,'pointerup',event());await e.save();
    assert.deepEqual(e.posts[0].elements[0].points,layerData().elements[0].points);
    assert.equal(e.node('[data-layer-undo]').disabled,true);
});

test('group selection applies style, copies and deletes as individual undoable operations',async()=>{
    const e=await editor(),data=layerData();data.elements.push({...structuredClone(data.elements[0]),id:'second'});
    await e.api.open(data);
    const choose=i=>{const check=e.node('[data-layer-elements]').children[i].children[0];check.checked=true;check.onchange()};
    choose(0);choose(1);assert.equal(e.tools.every(tool=>tool.disabled),true);
    e.setWidth(12);await e.save();assert.deepEqual(e.posts[0].elements.map(e=>e.width),[12,12]);
    e.node('[data-group-copy]').onclick();await e.save();
    assert.equal(e.posts[1].elements.length,4);assert.equal(new Set(e.posts[1].elements.map(e=>e.id)).size,4);
    e.node('[data-group-delete]').onclick();await e.save();assert.equal(e.posts[2].elements.length,2);
    e.node('[data-layer-undo]').onclick();await e.save();assert.equal(e.posts[3].elements.length,4);
});

test('group dragging moves all members together and cancels atomically',async()=>{
    const e=await editor(),data=layerData();data.elements.push({...structuredClone(data.elements[0]),id:'second',points:[[40,10],[41,11]]});
    await e.api.open(data);
    for(const row of e.node('[data-layer-elements]').children){row.children[0].checked=true;row.children[0].onchange()}
    const hit=()=>e.shapes.filter(s=>s.options?.opacity===.001).at(-1);
    emit(hit(),'pointerdown',event({shiftKey:true,clientY:40,clientX:10}));
    emit(e.doc,'pointermove',event({clientY:42,clientX:13}));emit(e.doc,'pointerup',event());await e.save();
    assert.deepEqual(e.posts[0].elements.map(e=>e.points[0]),[[52,23],[42,13]]);
    emit(hit(),'pointerdown',event({shiftKey:true,clientY:42,clientX:13}));
    emit(e.doc,'pointermove',event({clientY:43,clientX:14}));e.key('Escape');await e.save();
    assert.deepEqual(e.posts[1].elements,e.posts[0].elements);
    e.node('[data-layer-undo]').onclick();await e.save();assert.deepEqual(e.posts[2].elements.map(e=>e.points[0]),[[50,20],[40,10]]);
});

test('layer list previews one imported layer and exports the chosen whole-layer format',async()=>{
    const doc=new Node(),elements=new Map(),source=layerData(),saved=[],exports=[],requests=[];
    for(const selector of ['#layers-search','#layers-search-input','#layers-sort-button','#layers-sort-menu','[data-layers-list]','[data-layer-import]'])elements.set(selector,new Node());
    doc.querySelector=selector=>elements.get(selector)||null;doc.createElement=tag=>new Node(tag);
    doc.body=new Node();
    let approve=false;
    const win={addEventListener(){},innerWidth:1200,innerHeight:800,i18n:{locale:'en_US',t:key=>key},travelManagerDialogs:{yesNo:async()=>approve,choose:async()=> 'geojson'},
        travelManagerCustomLayers:{list:async()=>[source],save:async layer=>saved.push(layer)},
        travelManagerLayerApi:{request:async(url,options)=>{requests.push(url);return url.endsWith('/parse')?{layer:{...source,id:'import-copy'}}:{text:'complete layer',filename:'layer.geojson'}}},
        pywebview:{api:{read_layer_file:async()=>({status:'ok',text:'file',filename:'one.json'}),save_layer_file:async(text,filename)=>{exports.push({text,filename});return {status:'saved'}}}}};
    vm.runInNewContext(readFileSync('assets/js/views/layers.js','utf8'),{document:doc,window:win});
    doc.listeners['travel-manager:views-ready'][0]();await new Promise(resolve=>setImmediate(resolve));
    await elements.get('[data-layer-import]').onclick();assert.equal(saved.length,0);
    approve=true;await elements.get('[data-layer-import]').onclick();assert.equal(saved[0].id,'import-copy');
    const row=elements.get('[data-layers-list]').children[0];assert.equal(row.children.length,4);
    row.children.at(-1).onclick();
    await doc.body.children.at(-1).children[4].onclick();assert.equal(requests.at(-1),'/api/custom-layers/layer-1/export/geojson');
    assert.equal(exports[0].text,'complete layer');
});

test('points support notes and icons, coordinate editing, undo and safe text rendering',async()=>{
    const e=await editor();await e.api.open();e.draw('point');e.click([50,20]);
    assert.equal(e.api.isDrawing(),false);assert.equal(e.tools.every(tool=>tool.disabled),true);
    const list=e.node('[data-layer-elements]');
    const icon=list.children[1].children[1],note=list.children[2].children[1];
    icon.value='🚗';icon.onchange();note.value='<img src=x onerror=alert(1)>\nParking';note.onchange();
    const x=list.children[3].children[1].children[1];x.value='21';x.onchange();
    await e.save();const point=e.posts[0].elements[0];
    assert.equal(point.type,'point');assert.equal(point.icon,'🚗');assert.equal(point.note,note.value);
    assert.deepEqual(point.points,[[50,21]]);assert.deepEqual(point.segments,[]);
    assert.ok(e.shapes.filter(s=>s.content).at(-1).content.textContent.includes('<img'));
    e.node('[data-layer-undo]').onclick();await e.save();assert.deepEqual(e.posts[1].elements[0].points,[[50,20]]);
});

test('compact toolbar follows requested order and keeps status and back in sidebar',async()=>{
    const template=readFileSync('templates/panels/layer.html','utf8');
    const toolbar=template.split('class="layer-panel__drawing-toolbar"')[1].split('</div>')[0];
    const attributes=[...toolbar.matchAll(/data-(?:layer-(?:undo|redo|fit|close-curve|split|toggle-curve|snap|info)|element-delete|draw="[^"]+")/g)].map(m=>m[0]);
    assert.deepEqual(attributes,['data-layer-undo','data-layer-redo','data-layer-fit','data-draw="point"','data-draw="line"','data-draw="curve"','data-draw="route"','data-layer-close-curve','data-layer-split','data-layer-toggle-curve','data-element-delete','data-layer-snap','data-layer-info']);
    const e=await editor();assert.ok(e.panel.querySelector('[data-layer-status]'));assert.equal(e.toolsPanel.querySelector('[data-layer-status]'),null);
    await e.api.open(layerData());assert.equal(e.node('[data-layer-back]').hidden,true);e.select();assert.equal(e.node('[data-layer-back]').hidden,false);
    e.node('[data-layer-back]').onclick();assert.equal(e.node('[data-layer-back]').hidden,true);
});

test('snap toggle bypasses targets and selecting a segment highlights its two endpoints',async()=>{
    const e=await editor();await e.api.open(layerData());
    e.shapes.filter(s=>s.options?.opacity===.001).at(-1).listeners.click[0]({});
    const rows=()=>e.node('[data-layer-elements]').children.filter(row=>row.dataset.pointIndex!==undefined);
    assert.equal(rows().filter(row=>row.classList.contains('is-selected')).length,2);
    rows()[0].children[1].children[1].onfocus();
    assert.equal(rows().filter(row=>row.classList.contains('is-selected')).length,1);
    e.key('Escape');e.node('[data-layer-snap]').onclick();assert.equal(e.node('[data-layer-snap]').getAttribute('aria-pressed'),'false');
    e.draw('line');e.click([50.005,20.005]);e.click([53,23]);await e.save();
    assert.deepEqual(e.posts[0].elements[1].points[0],[50.005,20.005]);
    let info;e.win.travelManagerDialogs.yesNo=options=>{info=options};e.node('[data-layer-info]').onclick();
    assert.equal(info.information,true);assert.ok(info.description.includes('LAYER_EDITOR.SNAP_HINT'));
});

test('bulk controls select all, lock/unlock and hide as undoable edits',async()=>{
    const e=await editor(),data=layerData();data.elements.push({...structuredClone(data.elements[0]),id:'second',locked:true});
    await e.api.open(data);e.node('[data-group-all]').onclick();
    assert.equal(e.node('[data-layer-elements]').children.every(row=>row.children[0].checked),true);
    e.node('[data-group-lock]').onclick();await e.save();assert.equal(e.posts[0].elements.every(e=>e.locked),true);
    assert.equal(e.node('[data-group-delete]').disabled,true);
    e.node('[data-group-lock]').onclick();await e.save();assert.equal(e.posts[1].elements.every(e=>!e.locked),true);
    e.node('[data-group-hide]').onclick();await e.save();assert.equal(e.posts[2].elements.every(e=>e.hidden),true);
    e.node('[data-layer-undo]').onclick();await e.save();assert.equal(e.posts[3].elements.every(e=>!e.hidden),true);
    e.node('[data-group-all]').onclick();e.node('[data-group-all]').onclick();
    assert.equal(e.node('[data-layer-elements]').children.every(row=>!row.children[0].checked),true);
});

test('shape context menu follows requested order and includes dynamic icons',async()=>{
    const template=readFileSync('templates/panels/layer.html','utf8');
    const menu=template.split('data-layer-element-menu')[1].split('</aside>')[0];
    assert.deepEqual([...menu.matchAll(/data-element-menu-(\w+)/g)].map(m=>m[1]),['fit','duplicate','hidden','rename','locked','delete']);
    assert.equal((menu.match(/role="separator"/g)||[]).length,2);
    const e=await editor();await e.api.open(layerData());e.node('[data-layer-elements]').children[0].children.at(-1).onclick({stopPropagation(){}});
    assert.equal(e.node('[data-element-menu-hidden]').children[0].getAttribute('data-lucide'),'eye-off');
    assert.equal(e.node('[data-element-menu-locked]').children[0].getAttribute('data-lucide'),'lock');
});
