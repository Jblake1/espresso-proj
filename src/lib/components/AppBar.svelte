
<script>
    import { AppBar, LightSwitch } from '@skeletonlabs/skeleton';
    import { goto } from '$app/navigation';
    //import { LightSwitch } from '@skeletonlabs/skeleton';
    let color = 'primary';
    //let position = 'top'; // or 'bottom'
</script>

<style>
    .tabButton {
            background-color: #f1f1f1;
            border: none;
            color: black;
            padding: 5px 10px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
    }
</style>


<div>
    <AppBar color={color} >
        <div slot="lead">Espresso Oracle</div>

        <div slot="trail">
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
                <button onclick={() => goto('/about')}>About</button>
            </div>
        
            <div class="tabButton">
                <button onclick={() => goto('/register')}>Register</button>
            </div>

            <div>
                <LightSwitch />
            </div>
        </div>
    </AppBar>
</div>
   


