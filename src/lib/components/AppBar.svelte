
<script>
    import { AppBar, LightSwitch } from '@skeletonlabs/skeleton';
    import { goto } from '$app/navigation';
    import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
    import { onMount } from 'svelte';
    let color = 'primary';
    let currentPath = '';

    onMount(() => {
        currentPath = window.location.pathname;
    });

    function handleNavigation(event, path) {
        event.preventDefault(); // Prevent full page reload
        goto(path); // Use SvelteKit's client-side navigation
        currentPath = path; // Update the state
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
                <TabAnchor href="/" selected={currentPath === '/'} on:click={(e) => handleNavigation(e, '/')}>Home</TabAnchor>
                <TabAnchor href="/archive" selected={currentPath === '/archive'} on:click={(e) => handleNavigation(e, '/archive')}>Archive</TabAnchor>
                <TabAnchor href="/about" selected={currentPath === '/about'} on:click={(e) => handleNavigation(e, '/about')}>About</TabAnchor>
                <TabAnchor href="/login" selected={currentPath === '/login'} on:click={(e) => handleNavigation(e, '/login')}>Login</TabAnchor>
                <TabAnchor href="/register" selected={currentPath === '/register'} on:click={(e) => handleNavigation(e, '/register')}>Register</TabAnchor>
                <LightSwitch />
            </TabGroup>
        </svelte:fragment>
    </AppBar>
</div>
   


