<script>
  import { Plane } from "svelte-loading-spinners";

  const STATUS = {
    INITIAL_STATE: 0,
    LOADING: 1,
    LOADED: 2,
    ERROR: 3,
  };

  let step = {
      '1': STATUS.INITIAL_STATE,
      '2': STATUS.INITIAL_STATE
    }

  let images = {};

  const setImage = (name, image) => {
    let reader = new FileReader();
    reader.readAsDataURL(image);
    reader.onload = (e) => (images[name] = e.target.result);
  };

  const onFileSelected = async (e) => {
    let image = e.target.files[0];
    setImage("bn", image);

    let body = new FormData();
    body.append("image", image);

    step = {
      '1': STATUS.LOADING,
      '2': STATUS.LOADING
    }

    const url = "http://localhost:8080/colorize";

    const onReceiveColoredImg = (version) => async (data) => {
      if (data.ok) {
        const blob = await data.blob();
        setImage("color"+version, blob);
        step[version] = STATUS.LOADED;
      } else step[version] = STATUS.ERROR;
    }

    fetch(`${url}?version=v1`, { method: "POST", body }).then(onReceiveColoredImg('1'))
    fetch(`${url}?version=v2`, { method: "POST", body }).then(onReceiveColoredImg('2'))

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

    {#if step['1'] === STATUS.INITIAL_STATE}
      <div class="row">
        <div class="col-12">
          <h3>Choose your black and white image!</h3>
        </div>
      </div>
    {:else}
      <div class="row">
        <div class="col-4">
          <h2>Original</h2>
        </div>
        <div class="col-4">
          <h2>Colourised V1</h2>
        </div>
        <div class="col-4">
          <h2>Colourised V2</h2>
        </div>
      </div>

      <div class="row images">
        <div class="col-4">
          <img class="result" src={images["bn"]} alt="B/W original" />
        </div>
        {#each ['1','2'] as version}
        <div class="col-4">
          {#if step[version] === STATUS.LOADED}
            <img
              class="result"
              src={images["color"+version]}
              alt="Colourised result"
            />
          {:else if step[version] === STATUS.LOADING}
            <div class="loading">
              <p>Loading</p>
              <Plane size="60" color="#FF3E00" unit="px" duration="1s" />
            </div>
          {:else if step[version] === STATUS.ERROR}
            ERROR getting version {version}
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
</style>
