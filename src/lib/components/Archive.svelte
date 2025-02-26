<!-- base component of the archive page
 intends to show archived espresso setups 
 and allow for repeated updates to "journey cards" -->

 <script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import JourneyCard from './JourneyCard.svelte';
    
    let drink1 = '';
    let grinder1 = '';
    let grindSetting1 = '';
    let coffeeBeans1 = '';
    let brewingDevice1 = '';
    let iteration1 = '';
    let journey_id1 = '';
    let journey_id2 = '';
    let journey_id3 = '';

    let drink2 = '';
    let grinder2 = '';
    let grindSetting2 = '';
    let coffeeBeans2 = '';
    let brewingDevice2 = '';
    let iteration2 = '';

    let drink3 = '';
    let grinder3 = '';
    let grindSetting3 = '';
    let coffeeBeans3 = '';
    let brewingDevice3 = '';
    let iteration3 = '';

    let cardPropData1 = {};
    let cardPropData2 = {};
    let cardPropData3 = {};

    let cardProp1 = () => ({
        journeyID: journey_id1
    });

    let cardProp2 = () => ({
        journeyID: journey_id2
    });

    let cardProp3 = () => ({
        journeyID: journey_id3
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
                    journey_id1 = journeys[0].id;
                    cardPropData1 = cardProp1();
                }

                if (journeys.length > 1) {
                    // Destructure the second setup object
                    drink2 = journeys[1].drink;
                    grinder2 = journeys[1].grinder;
                    grindSetting2 = journeys[1].grindSetting;
                    coffeeBeans2 = journeys[1].coffeeBeans;
                    brewingDevice2 = journeys[1].brewingDevice;
                    iteration2 = journeys[1].iteration;
                    journey_id2 = journeys[1].id;
                    cardPropData2 = cardProp2();
                }

                if (journeys.length > 2) {
                    // Destructure the third setup object
                    drink3 = journeys[2].drink;
                    grinder3 = journeys[2].grinder;
                    grindSetting3 = journeys[2].grindSetting;
                    coffeeBeans3 = journeys[2].coffeeBeans;
                    brewingDevice3 = journeys[2].brewingDevice;
                    iteration3 = journeys[2].iteration;
                    journey_id3 = journeys[2].id;
                    cardPropData3 = cardProp3();
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
    .outerContainer {
        display: flex;
        flex-direction: row; /* Arrange elements in a row */
        align-items: flex-start; /* Align items at the top */
        gap: 10px; /* Add spacing between form and RecentSetups */
        width: 100%; /* Ensure the container takes up the full width */
    }

    .innerContainer {
        display: flex;
        flex-direction: column; /* Stack elements vertically */
        align-items: flex-start; /* Align items at the top */
        gap: 10px; /* Add spacing between form elements */
        width: 100%; /* Ensure the container takes up the full width */
    }

    .card {
        flex: 0 0 25%; /* Do not grow or shrink, take up 25% of the width */
    }

    .journeyCard {
        margin-top: 75px; /* Add margin above */
        flex: 1; /* Allow the journeyCard to take up remaining space */
    }
</style>

<div class="outerContainer">
    <div class="innerContainer">
        <div class="outerContainer"> 
            <div class="card p-4">
                <header class="card-header">Espresso Journey 1</header>
                <p>Drink: {drink1}</p>
                <p>Grinder: {grinder1}</p>
                <p>Coffee Beans: {coffeeBeans1}</p>
                <p>Brewing Device: {brewingDevice1}</p>
                <!-- <p>Journey ID: {journey_id1}</p> -->
                <footer class="card-footer text-center whitespace-nowrap">Grind Setting: {grindSetting1}</footer>
            </div>

            <div class="journeyCard">
                <JourneyCard journeyData={cardPropData1}/>
            </div>
        </div>

        <div class="outerContainer">
            <div class="card p-4">
                <h2>Espresso Journey 2</h2>
                <p>Drink: {drink2}</p>
                <p>Grinder: {grinder2}</p>
                <p>Grind Setting: {grindSetting2}</p>
                <p>Coffee Beans: {coffeeBeans2}</p>
                <p>Brewing Device: {brewingDevice2}</p>
                <!-- <p>Journey ID: {journey_id2}</p> -->
            </div>

            <div class="journeyCard">
                <JourneyCard journeyData={cardPropData2}/>
            </div>
        </div>

        <div class="outerContainer">
            <div class="card p-4">
                <h2>Espresso Journey 3</h2>
                <p>Drink: {drink3}</p>
                <p>Grinder: {grinder3}</p>
                <p>Grind Setting: {grindSetting3}</p>
                <p>Coffee Beans: {coffeeBeans3}</p>
                <p>Brewing Device: {brewingDevice3}</p>
                <!-- <p>Journey ID: {journey_id3}</p> -->
            </div>

            <div class="journeyCard">
                <JourneyCard journeyData={cardPropData3}/>
            </div>
        </div>
    </div>
</div>