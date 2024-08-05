<script lang="ts">
  import { writable } from "svelte/store";

  export let show = writable(false);

  const PATLink = "https://github.com/settings/tokens/new";

  function saveConfig() {
    const patInput = document.getElementById("patInput") as HTMLInputElement;
    localStorage.setItem("github_pat", patInput.value);
    show.set(false);
  }
</script>

<div class:invisible={!$show}>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
  <div class="fixed inset-0 overflow-y-auto">
    <div
      class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
    >
      <div
        class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:align-middle sm:max-w-lg sm:w-full"
      >
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                GitHub Personal Access Token Configuration
              </h3>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  Create a PAT with appropriate permissions from <a
                    href={PATLink}
                    target="_blank"
                    class="text-blue-600">here</a
                  >.
                </p>
                <input
                  id="patInput"
                  type="text"
                  placeholder="Enter your PAT here"
                  class="mt-2 p-2 border border-gray-300 rounded-md w-full"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            on:click={saveConfig}
            type="button"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 sm:ml-3 sm:w-auto sm:text-sm"
          >
            Save
          </button>
          <button
            on:click={() => show.set(false)}
            type="button"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .invisible {
    display: none;
  }
</style>
