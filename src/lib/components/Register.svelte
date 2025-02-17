<!-- Allow non existing user to register as a user
 provide username email password
 register and redirect to home
 include optional redirect to login -->

<script lang="ts">
    import { onMount } from 'svelte'
    import { selectOnFocus } from '../actions'
    import { goto } from '$app/navigation';
    

    let username = '';
    let email = '';
    let password = '';
    let confirmPassword = '';
    let errorMessage = '';

    // const dispatch = createEventDispatcher();

    const register = async () => {
        if (password !== confirmPassword) {
            errorMessage = 'Passwords do not match';
            return;
        }

        try {
            const response = await fetch('http://localhost:4000/register', {
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
                // Redirect to the home page
                window.location.href = '/login';
                } else {
                throw new Error('Registration failed');
                }
            }

            

        } catch (error) {
            errorMessage = error.message;
        }
    };
</script>

<style>
    .error {
        color: red;
    }
</style>

<form on:submit|preventDefault={register}>
    <h2>Register</h2>

    {#if errorMessage}
        <p class="error">{errorMessage}</p>
    {/if}

    <label for="username">Username</label>
    <input type="text" id="username" bind:value={username} required />

    <label for="email">Email</label>
    <input type="email" id="email" bind:value={email} required />

    <label for="password">Password</label>
    <input type="password" id="password" bind:value={password} required />

    <label for="confirmPassword">Confirm Password</label>
    <input type="password" id="confirmPassword" bind:value={confirmPassword} required />

    <button type="submit" class="btn btn__primary btn__lg">Register</button>
</form>

<!-- <div class="loginLink">
    <button onclick={() => goto('/login')}>Login</button>
</div> -->