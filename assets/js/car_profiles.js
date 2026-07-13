document.addEventListener('travel-manager:views-ready', () => {
    let profiles = [];
    let activeCarProfileId = null;
    let loaded = false;

    const notify = () => {
        const active = profiles.find((profile) => profile.id === activeCarProfileId) || null;

        document.dispatchEvent(new CustomEvent('travel-manager:car-profiles-changed', {
            detail: {
                activeCarProfile: active ? { ...active } : null,
                activeCarProfileId,
                profiles: profiles.map((profile) => ({ ...profile }))
            }
        }));
    };

    const list = async (force = false) => {
        if (loaded && !force) {
            return profiles;
        }

        const response = await fetch('/api/car-profiles', {
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) {
            throw new Error('Nie udało się wczytać profili samochodów.');
        }

        const data = await response.json();
        profiles = data.profiles || [];
        activeCarProfileId = data.active_car_profile_id || null;
        loaded = true;
        notify();
        return profiles;
    };

    const save = async (profile) => {
        const response = await fetch('/api/car-profiles', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(profile)
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data?.message || 'Nie udało się zapisać profilu samochodu.');
        }

        profiles = profiles.filter((item) => item.id !== data.profile.id);
        profiles.push(data.profile);
        activeCarProfileId = data.active_car_profile_id || activeCarProfileId;
        loaded = true;
        notify();
        return data.profile;
    };

    const remove = async (profileId) => {
        const response = await fetch(`/api/car-profiles/${encodeURIComponent(profileId)}`, {
            method: 'DELETE',
            headers: { 'Accept': 'application/json' }
        });
        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data?.message || 'Nie udało się usunąć profilu samochodu.');
        }

        profiles = profiles.filter((item) => item.id !== profileId);
        activeCarProfileId = data.active_car_profile_id || null;
        notify();
    };

    const setActive = async (profileId) => {
        const response = await fetch('/api/car-profiles/active', {
            method: 'PATCH',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ profile_id: profileId || null })
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data?.message || 'Nie udało się ustawić aktywnego samochodu.');
        }

        activeCarProfileId = data.active_car_profile_id || null;
        notify();
        return data.active_car_profile || null;
    };

    const active = () => profiles.find((profile) => profile.id === activeCarProfileId) || null;

    window.travelManagerCarProfiles = {
        active,
        list,
        remove,
        save,
        setActive
    };

    list().catch(() => {});
});
