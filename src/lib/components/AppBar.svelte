
<script lang="ts">
    import { AppBar, LightSwitch } from '@skeletonlabs/skeleton';
    import { goto } from '$app/navigation';
    import { TabGroup, TabAnchor, Avatar, popup } from '@skeletonlabs/skeleton';
    import type { PopupSettings } from '@skeletonlabs/skeleton';
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    
    // Create a store for user data
    const userStore = writable(null);
    
    let color = 'primary';
    let currentPath = '';
    let userInitials = 'P';

     // Define the popup settings
     const popupSettings: PopupSettings = {
        event: 'click',
        target: 'userMenu',
        placement: 'bottom-end'
    };

    // Get initials from a username string
    function getInitials(username: string): string {
        if (!username) return 'G';
        
        const nameParts = username.split(/[\s-]+/);
        if (nameParts.length === 1) {
            return username.substring(0, 2).toUpperCase();
        } else {
            return (nameParts[0][0] + nameParts[nameParts.length - 1][0]).toUpperCase();
        }
    }

    // Check auth status and get user data
    async function checkAuth() {
        try {
            // Try to get stored user data first (for quick UI loading)
            const storedUser = localStorage.getItem('user');
            if (storedUser) {
                const userData = JSON.parse(storedUser);
                $userStore = userData;
                userInitials = getInitials(userData.username);
            }
            
            // Then verify with server (in case token is invalid or expired)
            const response = await fetch('http://localhost:5000/verify-auth', {
                method: 'GET',
                credentials: 'include'  // Important to include cookies
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.authenticated) {
                    // Update with fresh data from server
                    $userStore = {
                        id: data.user_id,
                        username: data.username
                    };
                    userInitials = getInitials(data.username);
                    
                    // Update localStorage with fresh data
                    localStorage.setItem('user', JSON.stringify($userStore));
                } else {
                    // Clear if server says not authenticated
                    localStorage.removeItem('user');
                    $userStore = null;
                    userInitials = 'G';
                }
            } else {
                // Handle server error - could keep existing data or clear it
                console.error('Auth verification failed:', await response.text());
            }
        } catch (error) {
            console.error('Auth check error:', error);
            // On error, fall back to localStorage data (already handled above)
        }
    }

    onMount(() => {
        currentPath = window.location.pathname;
        checkAuth();
    });

    function handleNavigation(event, path) {
        event.preventDefault(); // Prevent full page reload
        goto(path); // Use SvelteKit's client-side navigation
        currentPath = path; // Update the state
    }

    async function handleLogout() {
        try {
            // Call logout endpoint to invalidate JWT cookie
            const response = await fetch('http://localhost:5000/logout', {
                method: 'POST',
                credentials: 'include'
            });
            
            // Clear local storage regardless of server response
            localStorage.removeItem('user');
            $userStore = null;
            userInitials = 'G';
            
            // Redirect to login page
            goto('/login');
        } catch (error) {
            console.error('Logout error:', error);
            // Still clear local data and redirect even if server call fails
            localStorage.removeItem('user');
            $userStore = null;
            goto('/login');
        }
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
                <div class="relative px-4">
                    <button class="btn-icon variant-ghost-surface z-50" use:popup={popupSettings}>
                        <Avatar initials={userInitials} />
                    </button>
                </div>
                
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
<div class="card p-4 w-60 shadow-xl fixed z-[1000]" data-popup="userMenu">
    <div class="list-nav">
        <ul>
            <li><a href="/login" class="menu-item" on:click={(e) => handleNavigation(e, '/login')}>Login</a></li>
            <li><a href="/register" class="menu-item" on:click={(e) => handleNavigation(e, '/register')}>Register</a></li>
            <li><button class="menu-item w-full text-left" on:click={handleLogout}>Logout</button></li>
        </ul>
    </div>
</div>


