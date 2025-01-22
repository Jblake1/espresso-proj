<script lang="ts">
    import { onMount } from 'svelte'
    import { selectOnFocus } from '../actions'
    

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
                    password
                })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Registration failed');
            }

            const data = await response.json();
            
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

    <button type="submit">Register</button>
</form>