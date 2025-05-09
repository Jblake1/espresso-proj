<!-- Allow non existing user to register as a user
 provide username email password
 register and redirect to home
 include optional redirect to login -->

 <script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    
    let username = '';
    let email = '';
    let password = '';
    let confirmPassword = '';
    let errorMessage = '';

    const register = async () => {
        if (password !== confirmPassword) {
            errorMessage = 'Passwords do not match';
            return;
        }

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username,
                    email,
                    password,
                    confirm_password: confirmPassword
                })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.message === "registration successful") {
                    console.log('Registration successful:', data);
                    // Redirect to the login page
                    goto('/login');
                } else {
                    throw new Error('Registration failed');
                }
            }
        } catch (error) {
            errorMessage = error.message;
        }
    };
</script>

<style></style>

<div class="flex justify-start pt-10 items-center min-h-screen">
    <div class="card p-4 w-[90%] sm:w-2/3 md:w-1/3">
        <form on:submit|preventDefault={register} class="space-y-4">
            <h2 class="h2">Register</h2>

            {#if errorMessage}
                <div class="alert variant-filled-error">{errorMessage}</div>
            {/if}

            <label class="label">
                <span>Username</span>
                <input 
                    class="input" 
                    type="text" 
                    bind:value={username} 
                    placeholder="Enter your username"
                    required 
                />
            </label>

            <label class="label">
                <span>Email</span>
                <input 
                    class="input" 
                    type="email" 
                    bind:value={email} 
                    placeholder="Enter your email"
                    required 
                />
            </label>

            <label class="label">
                <span>Password</span>
                <input 
                    class="input" 
                    type="password" 
                    bind:value={password} 
                    placeholder="Enter your password"
                    required 
                />
            </label>

            <label class="label">
                <span>Confirm Password</span>
                <input 
                    class="input" 
                    type="password" 
                    bind:value={confirmPassword} 
                    placeholder="Confirm your password"
                    required 
                />
            </label>

            <button type="submit" class="btn variant-filled-primary w-full">Register</button>
            <div class="flex items-center space-x-2">
                <span>Already have an account?</span>
                <a href="/login" class="text-blue-500 underline">Login</a>
            </div>
        </form>
    </div>
</div>