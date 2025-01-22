<script lang="ts">
    import { onMount } from 'svelte'
    import { selectOnFocus } from '../actions'
  
    let email = $state('');
    let password = $state('');
    let emailEl: HTMLInputElement;
    let passwordEl: HTMLInputElement;
    let errorMessage = $state('');
  
    const submit = async () => {
      try {
        const response = await fetch('http://localhost:4000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email,
            password
          })
        });
  
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Login failed: ${errorText}`);
        }
  
        const data = await response.json();
        console.log('Login successful:', data);
        
      } catch (error) {
        console.error('There was a problem with the login operation:', error);
        errorMessage = 'Login Unsuccessful. Please check email and password';
      }
    };
  
    const onCancel = () => {
      email = '';
      password = '';
      emailEl.focus();
    };
  
    onMount(() => {
      emailEl.focus();
    });
    
</script>

  
<style>
    .error-message {
        color: red;
        margin-top: 1em;
    }
</style>
  
<form >
    <h2 class="label-wrapper">
        <label for="email" class="label__lg">Email</label>
    </h2>
    <input bind:this={emailEl} type="email" id="email" name="email" placeholder="Email" bind:value={email} class="input input__lg" />

    <h2 class="label-wrapper">
        <label for="password" class="label__lg">Password</label>
    </h2>
    <input bind:this={passwordEl} type="password" id="password" name="password" placeholder="Password" bind:value={password} class="input input__lg" />

    {#if errorMessage}
        <div class="error-message">{errorMessage}</div>
    {/if}

    <button type="submit" class="btn btn__primary btn__lg">Login</button>
    <button type="button" onclick={onCancel} class="btn btn__secondary btn__lg">Cancel</button>
</form>