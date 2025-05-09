<!-- Login page which redirects to home upon login 
 returns error msgs for failed login
 redirect to register page for non existing users -->

 <script lang="ts">
  import { onMount } from 'svelte'
  import { selectOnFocus } from '../actions'

  let email = $state('');
  let password = $state('');
  let emailEl: HTMLInputElement;
  let passwordEl: HTMLInputElement;
  let errorMessage = $state('');

  const handleSubmit = async (event: SubmitEvent) => {
    event.preventDefault();
    try {
        const response = await fetch('/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email,
            password
          }),
          credentials: 'include' // Important for cookies
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);
    
        if (response.ok && data.login_success) {
          console.log('Login successful:', data);

        // Store user data in localStorage
        const userData = {
          id: data.user_id,
          username: data.username,
          email: data.email,
          tokenExpires: Date.now() + (180 * 1000), // 15 minutes
        };

        console.log('Storing user data:', userData);
        localStorage.setItem('user', JSON.stringify(userData));

        setTimeout(async () => {
        try {
          const authCheck = await fetch('/verify-auth', {
            method: 'GET',
            credentials: 'include'
          });
          
          const authData = await authCheck.json();
          console.log('Auth verification after login:', authData);
          
          if (!authData.is_authenticated) {
            console.warn('Warning: Server did not confirm authentication');
          }
          
          // Continue with redirect regardless
          window.location.href = '/';
        } catch (error) {
          console.error('Auth check error:', error);
          window.location.href = '/';
        }
      }, 100);
      

        } else {
          console.error('Login failed:', data.message);
          errorMessage = data.message || 'Login Unsuccessful. Please check email and password';
        }
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

  onMount(async () => {
    try {
      const authCheck = await fetch('/verify-auth', {
        method: 'GET',
        credentials: 'include'
      });
      
      const authData = await authCheck.json();
      console.log('Initial auth check:', authData);
      
      if (authData.is_authenticated) {
        // Already logged in, redirect to home
        window.location.href = '/';
      }
    } catch (error) {
      console.error('Auth check error:', error);
    }
  });
</script>


<style></style>

<div class="flex justify-start pt-10 items-center min-h-screen">
  <div class="card p-4 w-[90%] sm:w-2/3 md:w-1/3">
    <form onsubmit={handleSubmit} class="space-y-4">
        <h2 class="h2">Login</h2>

        {#if errorMessage}
            <div class="alert variant-filled-error">{errorMessage}</div>
        {/if}
        <label class="label">
            <span>Email</span>
            <input 
                class="input" 
                type="email" 
                bind:value={email}
                bind:this={emailEl}
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
                bind:this={passwordEl}
                placeholder="Enter your password"
                required
            />
        </label>

        <button type="submit" class="btn variant-filled-primary w-full">Login</button>
        <div class="flex items-center space-x-2">
            <span>Need an account?</span>
            <a href="/register" class="text-blue-500 underline">Register</a>
        </div>
    </form>
  </div>
</div>