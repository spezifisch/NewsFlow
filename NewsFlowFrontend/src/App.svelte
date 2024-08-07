<script lang="ts">
  import { onMount } from 'svelte'
  import ConfigDialog from './components/ConfigDialog.svelte'
  import { writable } from 'svelte/store'
  import axios from 'axios'

  const showConfig = writable(false)
  const feeds = writable([])
  const articles = writable([])
  const selectedFeed = writable(null)
  const githubToken = localStorage.getItem('github_pat')

  async function fetchArtifact() {
    const headers = {
      Authorization: `token ${githubToken}`,
      Accept: 'application/vnd.github.v3+json',
    }

    const runs = await axios.get(
      'https://api.github.com/repos/your-username/your-repo/actions/runs',
      { headers }
    )
    const runId = runs.data.workflow_runs[0].id

    const artifacts = await axios.get(
      `https://api.github.com/repos/your-username/your-repo/actions/runs/${runId}/artifacts`,
      { headers }
    )
    const artifactId = artifacts.data.artifacts[0].id

    const download = await axios.get(
      `https://api.github.com/repos/your-username/your-repo/actions/artifacts/${artifactId}/zip`,
      { headers, responseType: 'blob' }
    )

    const zip = new JSZip()
    const content = await zip.loadAsync(download.data)
    const fileContent = await content.files['rss_data.json'].async('string')

    const parsedData = JSON.parse(fileContent)
    feeds.set(parsedData.data.feeds)
    articles.set(parsedData.data.articles)
  }

  onMount(() => {
    if (githubToken) {
      fetchArtifact()
    } else {
      showConfig.set(true)
    }
  })

  function selectFeed(feedId) {
    selectedFeed.set(feedId)
  }
</script>

<ConfigDialog bind:show={$showConfig} />

<main class="flex h-screen">
  <div class="w-1/3 bg-gray-100 p-4">
    <button
      on:click={() => showConfig.set(true)}
      class="mb-4 p-2 bg-blue-600 text-white rounded-md">Settings</button
    >
    <ul>
      {#each $feeds as feed (feed.feed_id)}
        <li
          on:click={() => selectFeed(feed.feed_id)}
          class="cursor-pointer p-2 rounded-md hover:bg-gray-200"
        >
          {feed.feed_title}
        </li>
      {/each}
    </ul>
  </div>
  <div class="w-2/3 bg-white p-4">
    <ul>
      {#each $articles.filter((article) => $selectedFeed === null || article.feed_id === $selectedFeed) as article (article.title)}
        <li class="p-2 border-b border-gray-200">
          <h2 class="text-lg font-semibold">{article.title}</h2>
          <p class="text-sm text-gray-600">{article.summary}</p>
          <a href={article.link} target="_blank" class="text-blue-600"
            >Read more</a
          >
        </li>
      {/each}
    </ul>
  </div>
</main>

<style>
  /* Add your custom styles here */
</style>
