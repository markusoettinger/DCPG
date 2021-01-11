<script>
  import FormField from "@smui/form-field";
  import Slider from "@smui/slider";
  import Dialog, { Title, InitialFocus } from "@smui/dialog";
  import Select, { Option } from "@smui/select";
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
  import MenuSurface, { Anchor } from "@smui/menu-surface";
  import Textfield from "@smui/textfield";
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
  import { onMount } from 'svelte';

  //import './menu-surface.scss';
  // import { Label, Icon } from "@smui/common";
  //-----------------------------------------------
  import { v4 as uuidv4 } from "uuid";
  let sliderDialog;
  let sliderDialogStop;
  let accounts = new Map();
  let contracts = new Map();
  let newAccounts;
  let estimatedDuration = 100;
  let desiredkWh = 80;
  let offeredFlex = 80;
  let chargedkWh = 0;
  let flexFlow = 0;

  function getAccounts() {
    fetch("http://localhost:8000/getAccounts")
      .then((d) => d.json())
      .then((d) => {
        console.log(d)
        accounts= new Map()
        for ( const key in d) {
            accounts.set(key, d[key])
        }
        console.log(accounts)
        // TODO merge existing Accounts into Map with fake names
      }); // merge into existing accounts (we only get addresses.. so kinda useless)
  }

  function handleErrors(response) {
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
  }

  let inCharging = [];
  function getInCharging() {
    fetch("http://localhost:8000/inCharging")
      .then((d) => d.json())
      .then((d) => (inCharging = d)); // make safer 
  }

  function getBalance(userId) {
    // perhaps buffer the values
    fetch(`http://localhost:8000/balance/${userId}`)
      .then((d) => d.json())
      .then((d) => {
        console.log(d);
        let account = accounts.get(userId);
        account.balance = d;
        accounts.set(userId, account);
        accounts=accounts
      })
  }

  function createAccount(userId) {
    // const userId = uuidv4();
    console.log("creating account");
    fetch(`http://localhost:8000/createAccount/${userId}`)
      .then(handleErrors)
      .catch((e)=>{
        console.log(e)
      });
    getAccounts();
  }

  function startCharging(
    userId,
    chargerId,
    estimatedDuration,
    desiredkWh,
    offeredFlex
  ) {
    console.log(userId,chargerId,estimatedDuration,desiredkWh,offeredFlex)
    fetch(
      `http://localhost:8000/startCharging/${userId}/${chargerId}/${estimatedDuration.toFixed(0)}/${desiredkWh}/${offeredFlex}`
    )
      .then((d) => d.json())
      .then((d) => console.log(d));
  }

  function stopCharging(userId, chargerId, flexFlow, chargedkWh) {
    fetch(
      `http://localhost:8000/stopCharging/${userId}/${chargerId}/${flexFlow}/${chargedkWh}`
    )
      .then((d) => d.json())
      .then((d) => console.log(d));
  }

  let knownChargers = [
    "charger 1",
    "charger 2",
    "charger 3",
    "charger 4",
    "charger 5",
  ];

  //-----------------------------------------------
  let formSurface;
  let userName = "";
  let desiredFlex = "";
  let superText = "";
  let rand = 0;

  function getRand() {
    fetch("http://localhost:8000/rand")
      .then((d) => d.text())
      .then((d) => (rand = d));
  }

  let clicked = 0;


  onMount(async () => {
		getInCharging();
    getAccounts();
	});


  function weiToEth(wei) {
    console.log(wei, wei/1e18)
    return wei/1e18
    
    
  }
  // let accounts = [
  //   { userId: "123ing", name: "something else", flex: 100 },
  //   { userId: "some1245thing", name: "something else", flex: 100 },
  //   { userId: "some33thing", name: "something else", flex: 100 },
  //   { userId: "some32354thing", name: "something else", flex: 100 },
  //   { userId: "somawfsething", name: "something else", flex: 100 },
  //   { userId: "somdfsething", name: "something else", flex: 100 },
  // ];

  // function addAccount() {
  //   if (input) {
  //     accounts = [
  //       ...accounts,
  //       {
  //         text: input,
  //         id: Math.random().toString(36).substr(2, 9),
  //       },
  //     ];
  //   }
  //   input = "";
  // }

  // function removeAccount(id) {
  //   const index = accounts.findIndex((todo) => todo.id === id);
  //   accounts.splice(index, 1);
  //   accounts = accounts;
  // }

  // let activeAccount;

  // let chargings = [
  //   { id: "J---aiyznGQ", name: "Keyboard Cat" },
  //   { id: "z_AbfPXTKms", name: "Maru" },
  //   { id: "OUtn3pvWmpg", name: "Henri The Existential Cat" },
  //   { id: "J---ai1yznGQ", name: "Keyboar23d Cat" },
  //   { id: "z_Ab1fPXTKms", name: "M131aru" },
  //   { id: "OUtn31pvWmpg", name: "11Henri The Existential Cat" },
  // ];

  let selectedAccountId = "Stephen Hawking";
  // This value is updated when the component is initialized, based on the
  // selected Item's `selected` prop.
  let selectionIndex = null;
  let selectedChargerId;
  let addCharging = () => {};

</script>

<!-- </section> -->
<style>
  :global(html, body) {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    /* padding: 0; */
  }
  /* .card-container {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    min-height: 500px;
    min-width: 380px;
    background-color: #f8f822;
    margin-right: 20px;
    margin-bottom: 20px;
  } */
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

  * :global(.mdc-select) {
    width: 100%;
    margin-bottom: 5px;
  }

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

  .menu-bar {
    position: absolute;
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
    position: relative;
  }
</style>

<!-- <section style="--tw-bg-opacity: 1;
background-color: rgba(31, 41, 55, var(--tw-bg-opacity));"> -->
<div class="header">
  <!-- <img style="width: 150px; height: 150px;" src="logo.png" alt="logo" /> -->
  <h2 style="margin-left: 18px;">Charging Processes</h2>
  <div class="menu-bar">
    <Meta class="material-icons" on:click={getInCharging}>refresh</Meta>
  </div>
</div>

<div class="content-row">
  <div class="content-column-left">
    <div style="display: flex;justify-content: space-between;">
      <h3 style="padding-left:20px">Accounts</h3>
      <div style="margin: 12px 10px auto auto;">
        <Button on:click={() => formSurface.setOpen(true)}>
          Create New Account
        </Button>
        <MenuSurface bind:this={formSurface} anchorCorner="BOTTOM_LEFT">
          <div
            style="margin: 1em; display: flex; flex-direction: column; align-items: flex-end;">
            <Textfield bind:value={userName} label="User Name" />
            <Button
              style="margin-top: 1em;"
              on:click={() => {
                formSurface.setOpen(false);
                createAccount(userName);
                userName = '';
              }}>
              Submit
            </Button>
          </div>
        </MenuSurface>
      </div>
    </div>
    <List
      class="demo-list"
      twoLine
      avatarList
      singleSelection
      bind:selectedIndex={selectionIndex}>
      {#each Array.from(accounts.entries()) as [userId, account], j}
        <Item
          on:SMUI:action={() => (selectedAccountId = userId)}
          disabled={false}
          selected={selectedAccountId === userId}>
          <Graphic
            style="background-image: url(https://via.placeholder.com/40x40.png?text={userId
              .split(' ')
              .map((val) => val.substring(0, 1))
              .join('')});" />
          <Text>
            <PrimaryText>{userId}</PrimaryText>
            <SecondaryText>{account.address}</SecondaryText>
          </Text>
          <Meta class="material-icons" on:click={sliderDialog.open()}>
            settings
          </Meta>
        </Item>
      {/each}
    </List>
    <Dialog
      bind:this={sliderDialog}
      aria-labelledby="slider-title"
      aria-describedby="slider-content">
      <Title id="slider-title">Start Charging</Title>
      <Content id="slider-content">
        <div>
          <Select bind:value={selectedChargerId} label="Charging Station">
            {#each knownChargers as charger}
              <Option value={charger}>{charger}</Option>
            {/each}
          </Select>
        </div>
        <div>
          <FormField align="end" style="display: flex; flex-direction: column;">
            <Slider
              bind:value={estimatedDuration}
              use={[InitialFocus]}
              min={0}
              max={12}
              step={1}
              discrete
              displayMarkers />
            <span slot="label">Estimated Duration</span>
          </FormField>
        </div>
        <div>
          <FormField align="end" style="display: flex; flex-direction: column;">
            <Slider
              bind:value={desiredkWh}
              min={0}
              max={200}
              step={5}
              discrete
              displayMarkers />
            <span slot="label">Desired kWh</span>
          </FormField>
        </div>
        <div>
          <FormField align="end" style="display: flex; flex-direction: column;">
            <Slider
              bind:value={offeredFlex}
              min={0}
              max={10}
              step={1}
              discrete
              displayMarkers />
            <!-- TODO must check for maxium available flex for that account -->
            <span slot="label">Flex to Boost</span>
          </FormField>
        </div>
      </Content>
      <Actions>
        <Button
          action="accept"
          on:click={() => {
            startCharging(selectedAccountId, selectedChargerId, estimatedDuration, desiredkWh, offeredFlex);
            // contracts.set(userId, { userId, selectedChargerId, estimatedDuration, desiredkWh, offeredFlex});
            getInCharging();
            sliderDialog.close();
          }}>
          <Label>Start</Label>
        </Button>
        <Button action="cancel" on:click={sliderDialog.close()}>
          <Label>Cancel</Label>
        </Button>
      </Actions>
    </Dialog>
  </div>
  <div class="content-column-right" style="display: flex; flex-wrap: wrap;">
    {#each inCharging as chargingProcess, i}
      <div class="cards">
        <Card style="width: 400px;margin: 10px;background-color: #f0f0f0;">
          <PrimaryAction on:click={() => clicked++}>
            <Content class="mdc-typography--body2">
              <h2 class="mdc-typography--headline6" style="margin: 0;">
                Charging Process No. {i}
              </h2>
              <!-- <h3
                class="mdc-typography--subtitle2"
                style="margin: 0 0 10px; color: #888;">
                Contract ID:
                {chargingProcess.userID}
              </h3> -->
              <table style="width:100%">
                <thead>
                  <tr>
                    <th />
                    <th />
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>User ID:</strong></td>
                    <td style="text-align:right">
                      {chargingProcess.userID}
                    </td>
                  </tr>
                  <tr>
                    <td><strong>Charger ID:</strong></td>
                    <td style="text-align:right">
                      {chargingProcess.chargerID}
                    </td>
                  </tr>
                  <tr>
                    <td><strong>Charging Time:</strong></td>
                    <td style="text-align:right">
                      {chargingProcess.estimatedDuration}
                    </td>
                  </tr>
                  <tr>
                    <td><strong>Flexibility offered:</strong></td>
                    <td style="text-align:right">
                      {chargingProcess.availableFlex / 1e18}
                    </td>
                  </tr>
                </tbody>
              </table>
            </Content>
          </PrimaryAction>
          <div class="action-buttons">
            <Actions>
              <ActionButtons>
                <Button on:click={() => sliderDialogStop.open()}>
                  <Label>Stop Charging</Label>
                </Button>
              </ActionButtons>
            </Actions>
          </div>
        </Card>
        <Dialog
          bind:this={sliderDialogStop}
          aria-labelledby="slider-title"
          aria-describedby="slider-content">
          <Title id="slider-title">Stop Charging</Title>
          <Content id="slider-content">
            <div>
              <FormField
                align="end"
                style="display: flex; flex-direction: column;">
                <Slider
                  bind:value={chargedkWh}
                  min={0}
                  max={200}
                  step={5}
                  discrete
                  displayMarkers />
                <span slot="label">Charged kWh</span>
              </FormField>
            </div>
            <div>
              <FormField
                align="end"
                style="display: flex; flex-direction: column;">
                <Slider
                  bind:value={flexFlow}
                  min={0}
                  max={weiToEth(chargingProcess.availableFlex)}
                  step={1}
                  discrete
                  displayMarkers />
                <span slot="label">Flex used</span>
              </FormField>
            </div>
          </Content>
          <Actions>
            <Button
              action="accept"
              on:click={() => {
                stopCharging(chargingProcess.userID, chargingProcess.chargerID, flexFlow, chargedkWh);
                getInCharging();
                sliderDialogStop.close();
              }}>
              <Label>Stop</Label>
            </Button>
            <Button action="cancel" on:click={sliderDialogStop.close()}>
              <Label>Cancel</Label>
            </Button>
          </Actions>
        </Dialog>
      </div>
    {/each}
  </div>
</div>
