
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
    let userInitials = 'G';
    let authChecked = false;

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
            console.log("Checking authentication...");
            
            // Try to get stored user data first
            const storedUser = localStorage.getItem('user');
            if (storedUser) {
                try {
                    const userData = JSON.parse(storedUser);
                    $userStore = userData;
                    userInitials = getInitials(userData.username);
                    console.log("Loaded user from localStorage:", userData);
                    console.log("Set user initials to:", userInitials);
                } catch (e) {
                    console.error("Error parsing localStorage data:", e);
                    localStorage.removeItem('user');
                }
            } else {
                console.log("No user found in localStorage");
            }
            
            // Only check with server if we're in the browser
            if (typeof window !== 'undefined') {
                try {
                    const response = await fetch('http://localhost:4000/verify-auth', {
                        method: 'GET',
                        credentials: 'include',  // Important for cookies
                        headers: {
                            'Accept': 'application/json'
                        }
                    });
                    
                    console.log("Server response status:", response.status);
                    
                    if (response.ok) {
                        const data = await response.json();
                        console.log("Server auth response:", data);
                        
                        // Mark that we've checked auth
                        authChecked = true;
                        
                        if (data.authenticated) {
                            // Update with fresh data from server
                            $userStore = {
                                id: data.user_id,
                                username: data.username
                            };
                            
                            userInitials = getInitials(data.username);
                            console.log("Updated user initials to:", userInitials);
                            
                            // Update localStorage
                            localStorage.setItem('user', JSON.stringify($userStore));
                        } else {
                            console.log("Server says: not authenticated");
                            
                            // Only clear if we've checked with server
                            if (authChecked) {
                                localStorage.removeItem('user');
                                $userStore = null;
                                userInitials = 'G';
                            }
                        }
                    } else {
                        // Handle non-OK responses (like 422 errors)
                        console.warn(`Auth check failed with status: ${response.status}`);
                        
                        // Try to read the error response
                        try {
                            const errorData = await response.json();
                            console.warn("Auth error details:", errorData);
                        } catch (parseError) {
                            console.warn("Could not parse error response");
                        }
                        
                        // For auth errors, we should consider the user not authenticated
                        // but maintain localStorage data to avoid disrupting the UI
                        console.log("Keeping localStorage user data for now");
                    }
                } catch (fetchError) {
                    console.warn("Server verification unavailable:", fetchError);
                    // If server is unavailable, keep using localStorage data
                }
            }
        } catch (error) {
            console.error('Auth check error:', error);
        }
    }

    onMount(() => {
        currentPath = window.location.pathname;
        checkAuth();
        
        // Add event listener for storage changes (for multi-tab support)
        window.addEventListener('storage', (event) => {
            if (event.key === 'user') {
                console.log("LocalStorage 'user' changed in another tab, updating...");
                checkAuth();
            }
        });
    });

    function handleNavigation(event, path) {
        event.preventDefault(); // Prevent full page reload
        goto(path); // Use SvelteKit's client-side navigation
        currentPath = path; // Update the state

        // Re-check auth after navigation
        setTimeout(checkAuth, 100);
    }

    // Re-check auth periodically (every 10 seconds)
    let authInterval;
    onMount(() => {
        authInterval = setInterval(checkAuth, 10000);
        return () => clearInterval(authInterval);
    });

    // Check auth when userStore changes
    $: if ($userStore !== null) {
        console.log("UserStore changed:", $userStore);
        userInitials = getInitials($userStore.username);
    }


    async function handleLogout() {
        try {
            // Call logout endpoint to invalidate JWT cookie
            const response = await fetch('http://localhost:4000/logout', {
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
                        {#if $userStore}
                            <span class="badge-icon variant-filled-primary absolute -top-1 -right-1 z-10">✓</span>
                        {/if}
                    </button>
                </div>
                
                <TabAnchor href="/" selected={currentPath === '/'} on:click={(e) => handleNavigation(e, '/')}>Home</TabAnchor>
                <TabAnchor href="/archive" selected={currentPath === '/archive'} on:click={(e) => handleNavigation(e, '/archive')}>Archive</TabAnchor>
                <TabAnchor href="/about" selected={currentPath === '/about'} on:click={(e) => handleNavigation(e, '/about')}>About</TabAnchor>
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


