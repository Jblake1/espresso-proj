<script lang="ts">
    import { AppBar, LightSwitch } from '@skeletonlabs/skeleton';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { TabGroup, TabAnchor, Avatar, popup } from '@skeletonlabs/skeleton';
    import type { PopupSettings } from '@skeletonlabs/skeleton';
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    
    // Create a store for user data
    const userStore = writable(null);
    
    let color = 'primary';
    let userInitials = 'G';
    let authChecked = false;

    $: currentPath = $page.url.pathname;
    $: isHomePage = currentPath === '/';
    

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
            // console.log("Checking authentication..."); // Reduced logging
            
            // Try to get stored user data first
            const storedUser = localStorage.getItem('user');
            if (storedUser) {
                try {
                    const userData = JSON.parse(storedUser);
                    $userStore = userData;
                    userInitials = getInitials(userData.username);
                } catch (e) {
                    console.error("Error parsing localStorage data:", e);
                    localStorage.removeItem('user');
                }
            } 
            // else { // Reduced logging
            //     console.log("No user found in localStorage");
            // }
            
            // Only check with server if we're in the browser
            if (typeof window !== 'undefined') {
                try {
                    const response = await fetch('/verify-auth', {
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
                        
                        if (data.is_authenticated) {
                            // Update with fresh data from server
                            $userStore = {
                            id: data.user_id,
                            username: data.username
                        };
                            
                            userInitials = getInitials(data.username);
                            localStorage.setItem('user', JSON.stringify($userStore));
                            // console.log("Updated user initials to:", userInitials);
                        } else {
                            console.log("Server says: not authenticated");
                            localStorage.removeItem('user');
                            $userStore = null;
                            userInitials = 'G';
                        }
                    } else if (response.status === 401) {
                        // Token expired, try to refresh
                        console.log("Auth token expired, attempting refresh...");
                        // Placeholder for actual refresh logic
                        const refreshed = false; // Assume refresh fails for now
                        authChecked = true;
                        
                        if (refreshed) {
                            // If refresh succeeded, try auth check again
                            console.log("Token refreshed, checking auth again...");
                            await checkAuth(); // Re-check immediately
                        } else {
                            // If refresh failed, clear user data
                            console.log("Token refresh failed, logging out...");
                            localStorage.removeItem('user');
                            $userStore = null;
                            userInitials = 'G';
                        }
                    } else {
                        // Handle other non-OK responses
                        console.warn(`Auth check failed with status: ${response.status}`);
                        authChecked = true;
                    }
                } catch (error) {
                    console.error('Auth check error:', error);
                }
            }
        } catch (error) {
            console.error('Auth check error:', error);
            authChecked = true; // Mark as checked even if there's an error
        }
    }


    // Run checkAuth immediately on mount
    onMount(() => {
        // currentPath = $page.url.pathname;
        console.log('Current Path:', currentPath);
        console.log('isHomePage:', isHomePage);
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
        // currentPath = path;
        console.log('Navigated to:', currentPath); // Debugging

        // Re-check auth after navigation
        setTimeout(checkAuth, 100);
    }

    // Re-check auth periodically (every 10 seconds)
    let authInterval;
    onMount(() => {
        authInterval = setInterval(checkAuth, 300000);
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
            const response = await fetch('/logout', {
                method: 'POST',
                credentials: 'include'
            });
            
            // Clear local storage regardless of server response
            localStorage.removeItem('user');
            $userStore = null;
            userInitials = 'G';
            authChecked = true;
            
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
    <AppBar
        background={isHomePage ? 'bg-transparent' : 'bg-primary'}
        class={`grid-cols-3 ${isHomePage ? 'bg-white/80 backdrop-blur' : ''}`}
        slotDefault="place-self-center"
        slotTrail="place-content-end"
    >
        <svelte:fragment slot="lead">
            <a href="/" on:click={(e) => handleNavigation(e, '/')}>
                <strong class="text-xl uppercase">Java Booklet</strong>
            </a>
        </svelte:fragment>
        
        <svelte:fragment slot="trail">
            <div class="flex items-center space-x-2 sm:space-x-4 flex-wrap justify-end">
                <TabGroup regionList="flex space-x-1 sm:space-x-2">
                    <TabAnchor href="/recommendation" selected={currentPath === '/recommendation'} on:click={(e) => handleNavigation(e, '/recommendation')}>Brew</TabAnchor>
                    <TabAnchor href="/archive" selected={currentPath === '/archive'} on:click={(e) => handleNavigation(e, '/archive')}>Notes</TabAnchor>
                    <!-- <TabAnchor href="/" selected={currentPath === '/'} on:click={(e) => handleNavigation(e, '/')}>Home</TabAnchor> -->
                </TabGroup>
                
                <div class="relative">
                    <button class="btn-icon variant-ghost-surface" use:popup={popupSettings}>
                        <Avatar initials={userInitials} />
                        {#if $userStore}
                            <span class="badge-icon variant-filled-primary absolute -top-1 -right-1 z-10">✓</span>
                        {/if}
                    </button>
                </div>
            </div>
        </svelte:fragment>
    </AppBar>
</div>

<!-- User Menu Popup -->
<div class="card p-4 w-60 shadow-xl fixed z-[1000]" data-popup="userMenu">
    <nav class="list-nav">
        <ul>
            {#if $userStore}
                <li><button class="w-full text-left p-2 hover:bg-primary-500/10 rounded" on:click={handleLogout}>Logout</button></li>
                <li><div class="flex items-center"><LightSwitch /></div></li>
            {:else if authChecked}
                <li><a href="/login" class="w-full block p-2 hover:bg-primary-500/10 rounded" on:click={(e) => handleNavigation(e, '/login')}>Login</a></li>
                <li><a href="/register" class="w-full block p-2 hover:bg-primary-500/10 rounded" on:click={(e) => handleNavigation(e, '/register')}>Register</a></li>
                <li><div class="flex items-center"><LightSwitch /></div></li>
            {:else}
                <li><div class="p-2 text-center text-sm opacity-75">Loading...</div></li>
            {/if}
        </ul>
    </nav>
</div>


