
<script lang="ts">
    import { AppBar, LightSwitch } from '@skeletonlabs/skeleton';
    import { goto } from '$app/navigation';
    import { TabGroup, TabAnchor, Avatar, popup } from '@skeletonlabs/skeleton';
    import type { PopupSettings } from '@skeletonlabs/skeleton';
    import { onMount } from 'svelte';
    
    
    let color = 'primary';
    let currentPath = '';

     // Define the popup settings
     const popupSettings: PopupSettings = {
        event: 'click',
        target: 'userMenu',
        placement: 'bottom-end'
    };

    onMount(() => {
        currentPath = window.location.pathname;
    });

    function handleNavigation(event, path) {
        event.preventDefault(); // Prevent full page reload
        goto(path); // Use SvelteKit's client-side navigation
        currentPath = path; // Update the state
    }

    function handleLogout() {
        // Clear the user session
        localStorage.removeItem('user');
        // Redirect to the login page
        goto('/login');
    }
</script>

<style></style>

<div>
    <AppBar color={color}>
        <svelte:fragment slot="lead">
            <strong class="text-xl uppercase">Espresso Oracle</strong>
        </svelte:fragment>
        
        <svelte:fragment slot="trail">
            <TabGroup slot="justify-center">
                <button class="btn-icon variant-ghost-surface" use:popup={popupSettings}>
                    <Avatar initials="P" />
                </button>
                
                <TabAnchor href="/" selected={currentPath === '/'} on:click={(e) => handleNavigation(e, '/')}>Home</TabAnchor>
                <TabAnchor href="/archive" selected={currentPath === '/archive'} on:click={(e) => handleNavigation(e, '/archive')}>Archive</TabAnchor>
                <TabAnchor href="/about" selected={currentPath === '/about'} on:click={(e) => handleNavigation(e, '/about')}>About</TabAnchor>
                <!-- <TabAnchor href="/login" selected={currentPath === '/login'} on:click={(e) => handleNavigation(e, '/login')}>Login</TabAnchor>
                <TabAnchor href="/register" selected={currentPath === '/register'} on:click={(e) => handleNavigation(e, '/register')}>Register</TabAnchor> -->
                <LightSwitch />
            </TabGroup>
        </svelte:fragment>
    </AppBar>
</div>

<!-- User Menu Popup -->
<div class="card p-4 w-60 shadow-xl" data-popup="userMenu">
    <div class="list-nav">
        <ul>
            <li><a href="/login" class="menu-item" on:click={(e) => handleNavigation(e, '/login')}>Login</a></li>
            <li><a href="/register" class="menu-item" on:click={(e) => handleNavigation(e, '/register')}>Register</a></li>
            <li><button class="menu-item w-full text-left" on:click={handleLogout}>Logout</button></li>
        </ul>
    </div>
</div>


