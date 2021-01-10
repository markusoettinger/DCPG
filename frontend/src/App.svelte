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
  import MenuSurface, {Anchor} from '@smui/menu-surface';
  import Textfield from '@smui/textfield';
  import List, {
    Item,
    Text,
    Graphic,
    Separator,
    PrimaryText,
    SecondaryText,
    Meta,
  } from "@smui/list";
  import Fab from "@smui/fab";
  import HelperText from "@smui/textfield/helper-text";
  //import './menu-surface.scss';
  // import { Label, Icon } from "@smui/common";
  let formSurface;
  let userName = '';
  let desiredFlex = '';
  let superText = "";
  let rand = 0;

  function getRand() {
    fetch("http://localhost:8000/rand")
      .then((d) => d.text())
      .then((d) => (rand = d));
  }

  let clicked = 0;

  let accounts = [
    { id: "aa211", name: "something else", flex: 100 },
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
    font-family: Arial, Helvetica, sans-serif;
    /* padding: 0; */
  }
  .card-container {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    min-height: 500px;
    min-width: 380px;
    background-color: #f8f822;
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

  .menu-bar{
    position:absolute;
    top: 15px;
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
    height: 70px;
    position:relative;
  }

</style>

<!-- <section style="--tw-bg-opacity: 1;
background-color: rgba(31, 41, 55, var(--tw-bg-opacity));"> -->
<div class="header">
  <!-- <img style="width: 150px; height: 150px;" src="logo.png" alt="logo" /> -->
  <h2 style="margin-left: 18px;">Charging Processes</h2>
  <div class="menu-bar">
    <Button on:click={() => formSurface.setOpen(true)}>Create New Contract</Button>
    <MenuSurface bind:this={formSurface} anchorCorner="BOTTOM_LEFT">
      <div style="margin: 1em; display: flex; flex-direction: column; align-items: flex-end;">
        <Textfield bind:value={userName} label="User Name" />
        <Button style="margin-top: 1em;" on:click={() => formSurface.setOpen(false)}>Submit</Button>
      </div>
    </MenuSurface>
  </div>
  
</div>

<div class="content-row">
  <div class="content-column-left" style="position: relative;">
    <div style="display: flex;justify-content: space-between;">
      <h3 style="padding-left:20px">Accounts</h3>
      <Button on:click={() => formSurface.setOpen(true)} style="margin: auto 10px auto auto;">Create New Account</Button>
      <MenuSurface bind:this={formSurface} anchorCorner="BOTTOM_LEFT">
        <div style="margin: 1em; display: flex; flex-direction: column; align-items: flex-end;">
          <Textfield bind:value={userName} label="User Name" />
          <Button style="margin-top: 1em;" on:click={() => formSurface.setOpen(false)}>Submit</Button>
        </div>
      </MenuSurface>
    </div>
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
        </Item>
      {/each}
    </List>
  </div>
  <div class="content-column-right" style="display: flex; flex-wrap: wrap;">
    {#each chargings as chargingProcess, i}
    <div class="cards">
      <Card style="width: 400px;margin: 10px;background-color: #f0f0f0;">
        <PrimaryAction on:click={() => clicked++}>
          <Content class="mdc-typography--body2">
            <h2 class="mdc-typography--headline6" style="margin: 0;">
              Contract Number
              {i}.
            </h2>
            <h3
              class="mdc-typography--subtitle2"
              style="margin: 0 0 10px; color: #888;">
              Contract ID:
              {chargingProcess.id}.
            </h3>
            <table>
              <thead>
                <tr>
                  <th></th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>User ID:</strong></td>
                  <td style="text-align:right">{chargingProcess.name} {rand}</td>
                </tr>
                <tr>
                  <td><strong>Charger ID:</strong></td>
                  <td></td>
                </tr>
                <tr>
                  <td><strong>Charging Time:</strong></td>
                  <td></td>
                </tr>
                <tr>
                  <td><strong>Flexibility offered:</strong></td>
                  <td></td>
                </tr>
              </tbody>
            </table>
          </Content>
        </PrimaryAction>
        <div class="action-buttons">
          <Actions>
            <ActionButtons>
              <Button on:click={() => clicked++}>
                <Label>Stop Charging</Label>
              </Button>
            </ActionButtons>
          </Actions>
        </div>
      </Card>
    </div>
    {/each}
  </div>
</div>
<!-- </section> -->
