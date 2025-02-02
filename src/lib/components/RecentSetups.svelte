<script lang="ts">
    import { onMount } from 'svelte';

    let drink1 = $state('');
    let grinder1 = $state('');
    let grindSetting1 = $state('');
    let coffeeBeans1 = $state('');
    let brewingDevice1 = $state('');

    let drink2 = $state('');
    let grinder2 = $state('');
    let grindSetting2 = $state('');
    let coffeeBeans2 = $state('');
    let brewingDevice2 = $state('');

    let drink3 = $state('');
    let grinder3 = $state('');
    let grindSetting3 = $state('');
    let coffeeBeans3 = $state('');
    let brewingDevice3 = $state('');


    const displaySetups = async () => {
        try {
            const response = await fetch('http://localhost:4000/getSetup', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Recent setups:', data);
                const setups = data.setups;
                console.log('Setups:', setups);
            
            if (setups.length > 0) {
                // Destructure the first setup object
                drink1 = setups[0].drink;
                grinder1 = setups[0].grinder;
                grindSetting1 = setups[0].grindSetting;
                coffeeBeans1 = setups[0].coffeeBeans;
                brewingDevice1 = setups[0].brewingDevice;
            }

            if (setups.length > 1) {
                // Destructure the second setup object
                drink2 = setups[1].drink;
                grinder2 = setups[1].grinder;
                grindSetting2 = setups[1].grindSetting;
                coffeeBeans2 = setups[1].coffeeBeans;
                brewingDevice2 = setups[1].brewingDevice;
            }

            if (setups.length > 2) {
                // Destructure the third setup object
                drink3 = setups[2].drink;
                grinder3 = setups[2].grinder;
                grindSetting3 = setups[2].grindSetting;
                coffeeBeans3 = setups[2].coffeeBeans;
                brewingDevice3 = setups[2].brewingDevice;
            }
            } else {
                const error = await response.json();
                console.error('Failed to fetch recent setups:', error.message);
            }
           

        } catch (err) {
            console.error('Error fetching recent setups:', err);
        }
    }

    onMount(() => {
    displaySetups();
  });
</script>

<style>
    .container {
      display: flex;
      flex-direction: column;
      align-items: flex-end; /* Aligns items to the right */
      padding: 20px;
    }
  
    .setup {
      text-align: right; /* Aligns text to the right */
      margin-bottom: 20px;
    }
  </style>

<div class="container">
    <div class="setup">
      <h2>Recent Setup 1</h2>
      <p>Drink: {drink1}</p>
      <p>Grinder: {grinder1}</p>
      <p>Grind Setting: {grindSetting1}</p>
      <p>Coffee Beans: {coffeeBeans1}</p>
      <p>Brewing Device: {brewingDevice1}</p>
    </div>
  
    <div class="setup">
      <h2>Recent Setup 2</h2>
      <p>Drink: {drink2}</p>
      <p>Grinder: {grinder2}</p>
      <p>Grind Setting: {grindSetting2}</p>
      <p>Coffee Beans: {coffeeBeans2}</p>
      <p>Brewing Device: {brewingDevice2}</p>
    </div>
  
    <div class="setup">
      <h2>Recent Setup 3</h2>
      <p>Drink: {drink3}</p>
      <p>Grinder: {grinder3}</p>
      <p>Grind Setting: {grindSetting3}</p>
      <p>Coffee Beans: {coffeeBeans3}</p>
      <p>Brewing Device: {brewingDevice3}</p>
    </div>
  </div>