<script>
  import { Plane } from "svelte-loading-spinners";
  import Slider from "@bulatdashiev/svelte-slider";

  const headers = ["Original", "Colourised V1", "Colourised V2"];
  const versions = ["origin", "v1", "v2"];
  let data = undefined;

  const setImage = (version, blob) => {
    let reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onload = (e) => (data[version].image = e.target.result);
  };

  const onFileSelected = async (e) => {
    let image = e.target.files[0];
    data = { v1: {}, v2: {}, origin: {} };
    setImage("origin", image);

    let body = new FormData();
    body.append("image", image);

    const onReceiveColoredImg = (version) => async (result) => {
      if (result.ok) {
        const blob = await result.blob();
        setImage(version, blob);
        data[version].saturation = [100];
      } else data[version].error = true;
    };

    const colorizeVersion = async (version) =>
      fetch(`/api/colorize?version=${version}`, {
        // fetch(`http://localhost:8080/colorize?version=${version}`, {
        method: "POST",
        body,
      }).then(onReceiveColoredImg(version));

    colorizeVersion("v1");
    colorizeVersion("v2");
  };
</script>

<div class="l-site">
  <main class="l-main">
    <div class="row">
      <h1>Colourise!</h1>
    </div>

    <div class="row">
      <div class="col-12">
        <input
          type="file"
          accept=".jpg, .jpeg, .png"
          on:change={(e) => onFileSelected(e)}
        />
      </div>
    </div>

    {#if !data}
      <div class="row">
        <div class="col-12">
          <h3>Start by selecting a black and white picture.</h3>
        </div>
      </div>
    {:else}
      <div class="row">
        {#each headers as header}
          <div class="col-4">
            <h2>{header}</h2>
          </div>
        {/each}
      </div>
      <div class="row images">
        {#each versions as version}
          <div class="col-4">
            {#if !!data[version].image}
              <img
                class="result"
                src={data[version].image}
                alt={version}
                style="filter: saturate({data[version].saturation | 100}%);"
              />
            {:else if !!data[version].error}
              <p>
                Error getting version {version}
              </p>
            {:else}
              <div class="loading">
                <Plane size="60" color="#FF3E00" unit="px" duration="1s" />
              </div>
            {/if}
          </div>
        {/each}
      </div>
      <div class="row">
        {#each versions as version}
          <div class="col-4 slider">
            {#if !!data[version].saturation}
              <Slider max="300" bind:value={data[version].saturation} />
            {/if}
          </div>
        {/each}
      </div>
    {/if}
  </main>
</div>

<style lang="scss">
  $color: #ff3e00;

  h1,
  h2 {
    color: $color;
    text-transform: uppercase;
  }

  h1 {
    font-size: 4em;
    font-weight: 100;
    margin-top: 24px;
  }

  input {
    padding: 32px;
    border: 2px dotted lightgray;
    margin: 8px;
  }

  .row {
    &.images {
      align-items: center;
    }
  }

  .loading {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  img {
    width: 100%;
  }

  .row div.slider {
    --thumb-bg: #d33601;
    --progress-bg: #ff3e00;
  }
</style>
