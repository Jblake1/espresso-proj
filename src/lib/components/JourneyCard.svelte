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
    let cardData = $state([
        { datePosted: '', notes: '', grindSetting: '', shotTime: '', cardID: '', journeyID: '' },
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
            displayJourneyCard(props.journeyData.journeyID);
            
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

    // Function to format date to mm/dd/yy
    function formatDate(dateString) {
        if (!dateString) return '';
        
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return dateString; // Return original if invalid
        
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const year = date.getFullYear().toString().slice(-2);
        
        return `${month}/${day}/${year}`;
    }

    // Run the displayJourneyCard function when the prop journeyData.journeyID changes
    $effect(() => {
	console.log('running');
    console.log(props.journeyData.journeyID);

	if (props.journeyData.journeyID) {
		displayJourneyCard(props.journeyData.journeyID);
	}
    });

</script>

<style></style>

<!-- Updated layout with scroll snap -->
<div class="flex flex-row gap-2 w-full">
    <div class="flex items-center self-stretch">
        <button 
            class="rounded-full h-12 w-12 flex items-center justify-center bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold shadow"
            onclick={createJourneyCard}>
            <span class="text-xl">+</span>
        </button>
    </div>
    <!-- Scroll container with snap -->
    <div class="flex overflow-x-auto snap-x snap-mandatory pb-4 gap-4 w-full">
        {#each cardData as card, index}
            {#if card.cardID !== ''}
                <!-- Each card is a snap point -->
                <div class="snap-start shrink-0 w-80">
                    <form class="border border-gray-200 rounded-lg shadow-sm bg-white p-4 w-full">
                        <div class="mb-4">
                            <p class="text-sm font-medium text-gray-500">{formatDate(card.datePosted)}</p>
                        </div>
                        
                        <div class="mb-3">
                            <label for={`grindSetting${index + 1}`} class="block text-sm font-medium text-gray-700 mb-1">Grind Setting</label>
                            <input 
                                type="text" 
                                id={`grindSetting${index + 1}`} 
                                bind:value={card.grindSetting} 
                                required
                                class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500" 
                            />
                        </div>
                        
                        <div class="mb-3">
                            <label for={`shotTime${index + 1}`} class="block text-sm font-medium text-gray-700 mb-1">Shot Time</label>
                            <input 
                                type="text" 
                                id={`shotTime${index + 1}`} 
                                bind:value={card.shotTime} 
                                required 
                                class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                            />
                        </div>
                        
                        <div class="mb-4">
                            <label for={`notes${index + 1}`} class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
                            <textarea 
                                id={`notes${index + 1}`} 
                                bind:value={card.notes} 
                                required
                                class="w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 min-h-[80px]"
                            ></textarea>
                        </div>
                        
                        <button 
                            type="button" 
                            onclick={() => updateJourneyCard(index)}
                            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md shadow-sm">
                            Update
                        </button>
                    </form>
                </div>
            {/if}
        {/each}
    </div>
</div>
