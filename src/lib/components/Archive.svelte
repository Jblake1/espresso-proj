<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import JourneyCard from './JourneyCard.svelte';

    let drink1 = $state('');
    let grinder1 = $state('');
    let grindSetting1 = $state('');
    let coffeeBeans1 = $state('');
    let brewingDevice1 = $state('');
    let iteration1 = $state('');

    let drink2 = $state('');
    let grinder2 = $state('');
    let grindSetting2 = $state('');
    let coffeeBeans2 = $state('');
    let brewingDevice2 = $state('');
    let iteration2 = $state('');

    let drink3 = $state('');
    let grinder3 = $state('');
    let grindSetting3 = $state('');
    let coffeeBeans3 = $state('');
    let brewingDevice3 = $state('');
    let iteration3 = $state('');

    let cardProp = () => ({
        drink: drink1,
        grinder: grinder1,
        grindSetting: grindSetting1,
        coffeeBeans: coffeeBeans1,
        brewingDevice: brewingDevice1,
        iteration: iteration1
    });

    const displayArchive = async () => {
        try {
            const response = await fetch('http://localhost:4000/archiveSetup', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Archive:', data);
                const journeys = data.journeys;
                console.log('journeys:', journeys);
            
            if (journeys.length > 0) {
                // Destructure the first setup object
                drink1 = journeys[0].drink;
                grinder1 = journeys[0].grinder;
                grindSetting1 = journeys[0].grindSetting;
                coffeeBeans1 = journeys[0].coffeeBeans;
                brewingDevice1 = journeys[0].brewingDevice;
                iteration1 = journeys[0].iteration;
            }

            if (journeys.length > 1) {
                // Destructure the second setup object
                drink2 = journeys[1].drink;
                grinder2 = journeys[1].grinder;
                grindSetting2 = journeys[1].grindSetting;
                coffeeBeans2 = journeys[1].coffeeBeans;
                brewingDevice2 = journeys[1].brewingDevice;
                iteration2 = journeys[1].iteration;
            }

            if (journeys.length > 2) {
                // Destructure the third setup object
                drink3 = journeys[2].drink;
                grinder3 = journeys[2].grinder;
                grindSetting3 = journeys[2].grindSetting;
                coffeeBeans3 = journeys[2].coffeeBeans;
                brewingDevice3 = journeys[2].brewingDevice;
                iteration3 = journeys[2].iteration;
            }
            } else {
                const error = await response.json();
                console.error('Failed to fetch journeys:', error.message);
            }
           

        } catch (err) {
            console.error('Error fetching journeys:', err);
        }
    }


    onMount(() => {
    displayArchive();
    });
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

    .innerContainer {
    display: flex;
    flex-direction: column; /* Stack elements vertically */
    align-items: flex-start; /* Align items at the top */
    gap: 10px; /* Add spacing between form elements */
    width: 50%; /* Make form take 50% of the width */
  }

</style>

<h1>Archive</h1>

<div class="outerContainer">
    <div class="innerContainer">
        <div class="outerContainer"> 
            <div class="journey">
                <h2>Espresso Journey 1</h2>
                <p>Drink: {drink1}</p>
                <p>Grinder: {grinder1}</p>
                <p>Grind Setting: {grindSetting1}</p>
                <p>Coffee Beans: {coffeeBeans1}</p>
                <p>Brewing Device: {brewingDevice1}</p>
                <p>Iteration: {iteration1}</p>
            </div>

            <div class="JourneyCard">
                <JourneyCard journeyData={cardProp}/>
              </div>
        </div>

        <div class="outerContainer">
            <div class="journey">
                <h2>Espresso Journey 2</h2>
                <p>Drink: {drink2}</p>
                <p>Grinder: {grinder2}</p>
                <p>Grind Setting: {grindSetting2}</p>
                <p>Coffee Beans: {coffeeBeans2}</p>
                <p>Brewing Device: {brewingDevice2}</p>
                <p>Iteration: {iteration2}</p>
            </div>

            <div class="tabButton">
                <button onclick={()=>goto('/archive')}>+</button>
            </div>
        </div>

        <div class="outerContainer">
            <div class="journey">
                <h2>Espresso Journey 3</h2>
                <p>Drink: {drink3}</p>
                <p>Grinder: {grinder3}</p>
                <p>Grind Setting: {grindSetting3}</p>
                <p>Coffee Beans: {coffeeBeans3}</p>
                <p>Brewing Device: {brewingDevice3}</p>
                <p>Iteration: {iteration3}</p>
            </div>

            <div class="tabButton">
                <button onclick={()=>goto('/archive')}>+</button>
            </div>
        </div>
    </div>



    <div class="tabButton">
        <button onclick={() => goto('/login')}>Login</button>
    </div>

    <div class="tabButton">
        <button onclick={() => goto('/')}>Home</button>
    </div>

    <div class="tabButton">
        <button onclick={() => goto('/about')}>About</button>
    </div>

    <div class="tabButton">
        <button onclick={() => goto('/register')}>Register</button>
    </div>
</div>
