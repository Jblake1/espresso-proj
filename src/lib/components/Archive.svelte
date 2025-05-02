<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
    import JourneyCard from './JourneyCard.svelte';
    
    // Add loading state
    let isLoading = true;
    
    // Store all journeys in an array
    let journeys = [];
    
    // An array of background images to cycle through
    const journeyImages = [
        '/images/espresso1.jpg',
        '/images/espresso2.jpg',
        '/images/espresso3.jpg'
    ];

    const espresso_machine = '/images/espresso_machine.png';
    
    // Add state to track which accordion item is open
    let openItem = -1; // -1 means all closed

    // Function to toggle accordion items
    function toggleAccordion(index) {
        openItem = openItem === index ? -1 : index;
    }

    // Get image for a journey based on its index
    function getImageForIndex(index) {
        return journeyImages[index % journeyImages.length];
    }

    // Create card prop data for a journey
    function createCardPropData(journey) {
        return { journeyID: journey.id };
    }

    const deleteJourney = async (journeyID) => {
        try {
            const response = await fetch('/journeyDelete', {
                method: 'Post',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: journeyID
                }),
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Journey deleted:', data);
                // Refresh journeys after deletion
                displayArchive();
            } else {
                const error = await response.json();
                console.error('Failed to delete journey:', error.message);
            }
        } catch (err) {
            console.error('Error deleting journey:', err);
        }
    }

    const displayArchive = async () => {
        isLoading = true;
        try {
            const response = await fetch('/archiveSetup', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Archive:', data);
                journeys = data.journeys || [];
                console.log('journeys:', journeys);
            } else {
                const error = await response.json();
                console.error('Failed to fetch journeys:', error.message);
            }
        } catch (err) {
            console.error('Error fetching journeys:', err);
        } finally {
            isLoading = false;
        }
    }

    onMount(() => {
        displayArchive();
    });
</script>

<style>
    /* Keep existing styles */
    :global(.accordion-item) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        /* Add border to easily see item bounds */
        /* border: 1px solid red !important; */
    }

    :global(.accordion-item + .accordion-item) {
        margin-top: 1px !important;
    }

    /* --- ADD THESE OVERRIDES --- */

    /* 1. Reset Padding on Skeleton's Trigger */
    /* This allows your wrapper's px-2 to control the spacing */
    :global(.accordion-item .trigger) {
        padding: 0 !important;
        /* border: 1px dashed blue !important; */ /* Add border for debugging */
    }

    /* 2. Ensure the text container div can actually shrink */
    /* Target the div containing drink/separator/beans */
    :global(.accordion-item .trigger .summary-content-wrapper > div:first-of-type) {
        min-width: 0 !important; /* Force shrinking if overridden */
        /* border: 1px dashed lime !important; */ /* Add border for debugging */
    }

    /* 3. Explicitly re-apply truncate properties if needed (less likely) */
    :global(.accordion-item .trigger .summary-content-wrapper .coffee-bean-name) {
         /* Usually not needed if parents are correct, but uncomment if desperate */
         /* min-width: 0 !important; */
         /* overflow: hidden !important; */
         /* text-overflow: ellipsis !important; */
         /* white-space: nowrap !important; */
         /* border: 1px dashed yellow !important; */ /* Add border for debugging */
    }

    /* --- END OF NEW OVERRIDES --- */

    /* Existing img styles */
    img {
        max-height: 70vh;
        object-fit: contain;
        transition: transform 0.3s ease;
    }
</style>

<!-- removed gap of 7 from flex container -->
<div class="flex flex-row w-full justify-start">
    <div class="flex flex-col items-start w-full md:w-3/4">
        {#if isLoading}
            <div class="w-full flex justify-center items-center p-10">
                <div class="border-4 border-transparent border-t-primary-500 rounded-full w-10 h-10 animate-spin"></div>
            </div>
        {:else if journeys.length > 0}
        


            <div class="w-full max-w-md mx-auto my-4 p-2 border border-dashed border-gray-400"> <h3 class="text-center font-bold mb-2">Standalone Button Test</h3>
                <button
                    type="button"
                    class="flex items-center w-full h-10 px-2 justify-between border border-red-500 rounded"
                >
                    <div class="flex items-center space-x-2 overflow-hidden min-w-0 flex-1 border border-blue-500">
                        <p class="whitespace-nowrap bg-primary-500/80 px-2 py-0.5 rounded text-white text-xs flex-shrink-0">
                            Espresso
                        </p>
                        <div class="h-3 border-r border-slate-400 flex-shrink-0"></div>
                        <p class="truncate min-w-0 flex-1 bg-secondary-500/80 px-2 py-0.5 rounded text-white text-xs border border-green-500">
                            Super Long Ethiopia Yirgacheffe Gedeb Natural Process Name That Needs Ellipsis
                        </p>
                    </div>
            
                    <div class="flex-shrink-0 ml-2 border border-purple-500"> <span
                            class="btn-icon btn-sm variant-filled-error cursor-pointer p-1"
                            role="button"
                            aria-label="Delete item"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                            </svg>
                        </span>
                    </div>
                </button>
            </div>
       
            <Accordion class="w-full">
                {#each journeys as journey, index}
                    <AccordionItem open={openItem === index} class="mb-0">
                        <svelte:fragment slot="summary">
                            <div
                                class="summary-content-wrapper flex items-center w-full h-10 px-2 justify-between"
                                style="background-image: linear-gradient(to right, rgba(0,0,0,0.6), rgba(0,0,0,0.2)), url({getImageForIndex(index)}); background-size: cover; background-position: center;"
                                on:click|stopPropagation={() => toggleAccordion(index)}
                                on:keydown={(e) => e.key === 'Enter' && toggleAccordion(index)}
                                role="button"
                                tabindex="0"
                                aria-label="Toggle journey details for {journey.drink}"
                            >
                                <div class="flex items-center space-x-2 overflow-hidden min-w-0 flex-1">
                                    <p class="whitespace-nowrap bg-primary-500/80 px-2 py-0.5 rounded text-white text-xs flex-shrink-0">
                                        {journey.drink}
                                    </p>
                                    <div class="h-3 border-r border-white/60 flex-shrink-0"></div>
                                    <p class="coffee-bean-name truncate min-w-0 flex-1 bg-secondary-500/80 px-2 py-0.5 rounded text-white text-xs">
                                        {journey.coffeeBeans}
                                    </p>
                                </div>

                                <div class="flex-shrink-0 ml-2">
                                    <span
                                        class="btn-icon btn-sm variant-filled-error cursor-pointer p-1 flex items-center justify-center"
                                        on:click|stopPropagation={() => deleteJourney(journey.id)}
                                        on:keydown|stopPropagation={(e) => e.key === 'Enter' && deleteJourney(journey.id)}
                                        tabindex="0"
                                        role="button"
                                        aria-label="Delete journey {journey.drink} - {journey.coffeeBeans}"
                                    >
                                        <svg class="delete-icon" xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 0 24 24" width="18px" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zm2.46-7.12l1.41-1.41L12 12.59l2.12-2.12 1.41 1.41L13.41 14l2.12 2.12-1.41 1.41L12 15.41l-2.12 2.12-1.41-1.41L10.59 14l-2.13-2.12zM15.5 4l-1-1h-5l-1 1H5v2h14V4z"/></svg>
                                        </span>
                                </div>
                            </div>
                        </svelte:fragment>


                        <!-- <svelte:fragment slot="summary">
                            <button
                                type="button"
                                class="flex items-center w-full min-w-0 text-left h-10 p-0 pr-2 justify-between"
                                style="background-image: url({getImageForIndex(index)}); background-size: cover; background-position: center;"
                                on:click|stopPropagation={() => toggleAccordion(index)}
                                on:keydown={(e) => e.key === 'Enter' && toggleAccordion(index)}
                            >
                                <div class="py-0 px-3 rounded-md flex items-center space-x-3 overflow-hidden min-w-0 flex-1"> 
                                    <p class="whitespace-nowrap bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm flex-shrink-0">{journey.drink}</p>
                                    <div class="h-3 border-r border-slate-300 flex-shrink-0"></div>
                                    <p class="whitespace-nowrap truncate min-w-0 bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm flex-1">
                                        {journey.coffeeBeans}
                                    </p>
                                </div>
                               
                                <div class="flex-shrink-0"> 
                                    <span 
                                        class="btn-icon variant-filled-primary cursor-pointer"
                                        on:click|stopPropagation={() => deleteJourney(journey.id)}
                                        on:keydown|stopPropagation={(e) => e.key === 'Enter' && deleteJourney(journey.id)}
                                        tabindex="0"
                                        role="button"
                                        aria-label="Delete journey"
                                    >
                                        delete
                                    </span>
                                </div>
                            </button>
                        </svelte:fragment> -->





                        <svelte:fragment slot="content">
                            <div class="w-full">
                                <!-- removed "overflow-hidden" -->
                                <div class="w-full rounded-md"> 
                                    <div class="flex items-center justify-center">
                                        <div class="flex items-center space-x-3 flex-wrap">
                                            <p class="whitespace-nowrap">{journey.drink}</p>
                                            <div class="h-4 border-r border-slate-300"></div>
                                            <p class="whitespace-nowrap">{journey.coffeeBeans}</p>
                                            <div class="h-4 border-r border-slate-300"></div>
                                            <p class="whitespace-nowrap">{journey.grinder}</p>
                                            <div class="h-4 border-r border-slate-300"></div>
                                            <p class="whitespace-nowrap">{journey.brewingDevice}</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex justify-center w-full">
                                    <div class="w-full md:w-3/4">
                                        <JourneyCard journeyData={createCardPropData(journey)}  drink={journey.drink}/>
                                    </div>
                                </div>
                            </div>
                        </svelte:fragment>
                    </AccordionItem>
                {/each}
            </Accordion>
        {:else}
            <div class="w-full text-center p-10 border border-primary-200 rounded-lg bg-tertiary-900/50">
                <p class="text-xl font-semibold text-tertiary-200">No Notes</p>
                <p class="mt-2 text-tertiary-400">No coffee records have been created yet!?</p>
                <a href="/" class="btn variant-filled-primary mt-6">Get a setting recommendation</a>
            </div>
        {/if}
    </div>

    <!-- Right side: Fixed espresso machine image -->
    <div class="hidden md:block w-1/4 relative">
        <div class="p-4">
            <img src={espresso_machine} alt="Espresso Machine" class="w-full max-w-xs mx-auto drop-shadow-xl" />
        </div>
    </div>
</div>

