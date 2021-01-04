<script>
  import Card, {
    Content,
    PrimaryAction,
    Media,
    MediaContent,
    Actions,
    ActionButtons,
    ActionIcons,
  } from "@smui/card";
  import Button, { Label } from "@smui/button";
  import IconButton, { Icon } from "@smui/icon-button";
  import List, {
    Item,
    Text,
    Graphic,
    PrimaryText,
    SecondaryText,
    Meta,
  } from "@smui/list";
  // import Button from "@smui/button";
  import Fab from "@smui/fab";
  import Textfield from "@smui/textfield";
  import HelperText from "@smui/textfield/helper-text";
  // import { Label, Icon } from "@smui/common";

  let superText = "";
  let rand = 0;

  function getRand() {
    fetch("http://localhost:8000/rand")
      .then((d) => d.text())
      .then((d) => (rand = d));
  }

  let clicked = 0;

  let accounts = [
    { id: "123ing", name: "something else", flex: 100 },
    { id: "some1245thing", name: "something else", flex: 100 },
    { id: "some33thing", name: "something else", flex: 100 },
    { id: "some32354thing", name: "something else", flex: 100 },
    { id: "somawfsething", name: "something else", flex: 100 },
    { id: "somdfsething", name: "something else", flex: 100 },
  ];

  function addAccount() {
    if (input) {
      accounts = [
        ...accounts,
        {
          text: input,
          id: Math.random().toString(36).substr(2, 9),
        },
      ];
    }
    input = "";
  }

  function removeAccount(id) {
    const index = accounts.findIndex((todo) => todo.id === id);
    accounts.splice(index, 1);
    accounts = accounts;
  }

  let chargings = [
    { id: "J---aiyznGQ", name: "Keyboard Cat" },
    { id: "z_AbfPXTKms", name: "Maru" },
    { id: "OUtn3pvWmpg", name: "Henri The Existential Cat" },
    { id: "J---ai1yznGQ", name: "Keyboar23d Cat" },
    { id: "z_Ab1fPXTKms", name: "M131aru" },
    { id: "OUtn31pvWmpg", name: "11Henri The Existential Cat" },
  ];

  let selectedAccountId = "Stephen Hawking";
  // This value is updated when the component is initialized, based on the
  // selected Item's `selected` prop.
  let selectionIndex = null;
  let addCharging = () => {};
</script>

<style>
  :global(html, body) {
    margin: 0;
    /* padding: 0; */
  }
  .card-container {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    min-height: 500px;
    min-width: 380px;
    background-color: #f8f8f8;
    margin-right: 20px;
    margin-bottom: 20px;
  }
  /* .card-container.short {
    min-height: 200px;
  } */
  * :global(.card-media-16x9) {
    background-image: url(https://via.placeholder.com/320x180.png?text=16x9);
  }
  * :global(.card-media-square) {
    background-image: url(https://via.placeholder.com/320x320.png?text=square);
  }

  .content-row {
    display: flex;
  }
  /* 
  .content-column {
    flex: 50%;
  } */

  /* Responsive layout - makes a one column layout instead of a two-column layout */
  @media (max-width: 1280px) {
    .content-row {
      flex-direction: column;
    }
  }

  .content-column-left {
    flex: 100%;
    overflow: auto;
  }
  .content-column-right {
    flex: 100%;
    overflow: auto;
  }

  .fabcontainer{
    position:absolute;
    bottom: 50px;
    right: 50px;
    z-index: 999;
  }

  @media screen and (min-width: 1280px) {
    .content-column-left {
      flex: 30%;
    }
  }
  @media screen and (min-width: 1280px) {
    .content-column-right {
      flex: 70%;
    }
  }

  .header {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    background-color: #78be7c;
  }
</style>

<!-- <section style="--tw-bg-opacity: 1;
background-color: rgba(31, 41, 55, var(--tw-bg-opacity));"> -->
<div class="header">
  <!-- <img style="width: 150px; height: 150px;" src="logo.png" alt="logo" /> -->
  <h2 style="margin-left: 18px;">Charging Processes</h2>
</div>

<div class="content-row">
  <div class="content-column-left" style="position: relative;">
    <pre class="status">Selected: {selectedAccountId}, value of selectedIndex: {selectionIndex}</pre>
    <List
      class="demo-list"
      twoLine
      avatarList
      singleSelection
      bind:selectedIndex={selectionIndex}>
      {#each accounts as account, j}
        <Item
          on:SMUI:action={() => (selectedAccountId = account.id)}
          disabled={false}
          selected={selectedAccountId === account.id}>
          <Graphic
            style="background-image: url(https://via.placeholder.com/40x40.png?text={account.id
              .split(' ')
              .map((val) => val.substring(0, 1))
              .join('')});" />
          <Text>
            <PrimaryText>{account.id}</PrimaryText>
            <SecondaryText>{account.name}</SecondaryText>
          </Text>
          <Meta class="material-icons" on:click={getRand}>settings</Meta>
        </Item>
      {/each}
    </List>
    <div class="fabcontainer">

      <Fab on:click={getRand}><Icon class="material-icons">add</Icon></Fab>
    </div>
  </div>
  <div class="content-column-right" style="display: flex; flex-wrap: wrap;">
    {#each chargings as chargingProcess, i}
      <Card style="width: 360px;margin: 10px;background-color: #f0f0f0;">
        <PrimaryAction on:click={() => clicked++}>
          <Media class="card-media-16x9" aspectRatio="16x9" />
          <Content class="mdc-typography--body2">
            <h2 class="mdc-typography--headline6" style="margin: 0;">
              Card Number
              {i}.
            </h2>
            <h3
              class="mdc-typography--subtitle2"
              style="margin: 0 0 10px; color: #888;">
              Contract id is:
              {chargingProcess.id}.
            </h3>
            This contract is under the Name of
            {chargingProcess.name} {rand}
          </Content>
        </PrimaryAction>
        <Actions>
          <ActionButtons>
            <Button on:click={() => clicked++}>
              <Label>Action</Label>
            </Button>
            <Button on:click={() => clicked++}>
              <Label>Another</Label>
            </Button>
          </ActionButtons>
          <ActionIcons>
            <IconButton
              on:click={() => clicked++}
              toggle
              aria-label="Add to favorites"
              title="Add to favorites">
              <Icon class="material-icons" on>favorite</Icon>
              <Icon class="material-icons">favorite_border</Icon>
            </IconButton>
            <IconButton
              class="material-icons"
              on:click={() => clicked++}
              title="Share">
              share
            </IconButton>
            <IconButton
              class="material-icons"
              on:click={() => clicked++}
              title="More options">
              more_vert
            </IconButton>
          </ActionIcons>
        </Actions>
      </Card>
    {/each}
  </div>
</div>
<!-- </section> -->
