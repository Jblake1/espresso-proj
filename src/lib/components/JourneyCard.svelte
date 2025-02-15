<!-- recieve journey id from svelte
    return list of journey cards
    iterate through list of journey cards
    display each journey card (up to 3)
    indicate if there are more cards and count how many 
    add a button to view more cards
    make some field on cards editable (edits update in db)
     -->

<script lang="ts">
    import { onMount } from "svelte";
    
    // Props that can be passed from the parent Archive component
    let props = $props();

    let testVariable = $state('test');

    let bob = $state('bob');

    let journeyCards = $state([]);
    let journeyID = $state(props.journeyData.journeyID);
    let journeyPropData = () => props.journeyData.journeyID;
    let cardData = $state([
        { datePosted: '', notes: '', grindSetting: '', shotTime: '', cardID: '', journeyID: '' },
        { datePosted: '', notes: '', grindSetting: '', shotTime: '', cardID: '', journeyID: '' },
        { datePosted: '', notes: '', grindSetting: '', shotTime: '', cardID: '', journeyID: '' }
    ]);

    

    const createJourneyCard = async () => {
        try {
            const response = await fetch('http://localhost:4000/journeyCard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    journeyID: props.journeyData.journeyID
            })
        });

            if (!response.ok) {
                throw new Error('Network response of journeyCard not ok');
            }
            
        } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while posting the journey card.');
        }
    }

    const displayJourneyCard = async (journeyData) => {
        try {
            console.log(`Sending journeyID: ${journeyData}`);
            const response = await fetch(`http://localhost:4000/journeyCard?journeyID=${journeyData}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            
            if (response.ok) {
                const data = await response.json();
                console.log('JourneyCards:', data);
                const journeyCards = data.journeyCards;
                console.log('JourneyCardsData:', journeyCards);

                journeyCards.forEach((card, index) => {
                    if (index < cardData.length) {
                        
                        cardData[index].cardID = card.id;
                        cardData[index].datePosted = card.datePosted;
                        cardData[index].notes = card.notes;
                        cardData[index].grindSetting = card.grindSetting;
                        cardData[index].shotTime = card.shotTime;
                        cardData[index].journeyID = props.journeyData.journeyID;
                    }
                });
            }
        } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while getting the journey.');
        }
    };

    const updateJourneyCard = async (index) => {
        try {
            const response = await fetch('http://localhost:4000/journeyCardEdit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: cardData[index].cardID,
                    grindSetting: cardData[index].grindSetting,
                    shotTime: cardData[index].shotTime,
                    notes: cardData[index].notes
                })
            });

            if (!response.ok) {
                throw new Error('Network response of journeyCard update not ok');
            }

            } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while updating card.');
        }
    };

    // Run the displayJourneyCard function when the prop journeyData.journeyID changes
    $effect(() => {
	console.log('running');
    console.log(props.journeyData.journeyID);

	if (props.journeyData.journeyID) {
		displayJourneyCard(props.journeyData.journeyID);
	}
    });

</script>

<style>
    .journey-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .toDoForm {
    flex: 0.7; /* Take up all available space */
    margin-right: 0;
    }

    .card_text {
        font-size: 0.9rem;
        color: #666;
        margin: 0 0 0.5rem 0;
    }

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

<div class="outerContainer">
    <div class="tabButton">
        <button onclick={createJourneyCard}>+</button>
    </div>

    {#each cardData as card, index}
        {#if card.cardID !== ''}
            <div class="innerContainer">
                <p class="card_text">card ID {card.cardID}</p>
                <p class="card_text">date posted: {card.datePosted}</p>
                <p class="card_text">Journey id: {card.journeyID}</p>

                <form class="toDoForm">
                    <input type="text" id={`grindSetting${index + 1}`} bind:value={card.grindSetting} required />
                    <input type="text" id={`shotTime${index + 1}`} bind:value={card.shotTime} required />
                    <input type="text" id={`notes${index + 1}`} bind:value={card.notes} required />
                    <button type="submit" disabled={false} class="btn btn__primary btn__lg" onclick={() => updateJourneyCard(index)}>Update</button>
                </form>
            </div>
        {/if}
    {/each}
</div>
