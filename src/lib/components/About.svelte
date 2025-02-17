<!-- Placeholder -->
<script lang="ts">
    import { onMount } from 'svelte';
    import {goto} from '$app/navigation';

</script>


<style>

.tabButton {
        background-color: #f1f1f1;
        border: none;
        color: black;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }

    .outerContainer {
      display: flex;
      flex-direction: row; /* Arrange elements in a row */
      align-items: flex-start; /* Align items at the top */
      gap: 10px; /* Add spacing between form and RecentSetups */
    }

</style>

<form>
    <h1>About</h1>
    <p>Standard "about" page</p>
</form>

<div class = "container">
    <div class="tabButton">
        <button onclick={() => goto('/login')}>Login</button>
    </div>

    <div class="tabButton">
        <button onclick={() => goto('/')}>Home</button>
    </div>

    <div class="tabButton">
        <button onclick={() => goto('/archive')}>Archive</button>
    </div>

    <div class="tabButton">
        <button onclick={() => goto('/register')}>Register</button>
    </div>
</div>