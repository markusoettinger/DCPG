<script>
  import FormField from "@smui/form-field";
  import Slider from "@smui/slider";
  import Dialog, { Title, InitialFocus } from "@smui/dialog";
  import Select, { Option } from "@smui/select";
  import Card, {
    Content,
    PrimaryAction,
    Actions,
    ActionButtons,
  } from "@smui/card";
  import Button, { Label } from "@smui/button";
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
  import { onMount } from "svelte";

  //import './menu-surface.scss';
  // import { Label, Icon } from "@smui/common";
  //-----------------------------------------------

  let sliderDialog;
  let sliderDialogStop;
  let accounts = new Map();
  let estimatedDuration = 1;
  let desiredkWh = 80;
  let offeredFlex = 2;
  let chargedkWh = 0;
  let flexFlow = 0;
  let selectedAvailableFlex = 0;
  let formSurface;
  let userName = "";

  function handleErrors(response) {
    if (!response.ok) {
      throw Error(response.statusText);
    }
    return response;
  }

  // callback functions for communicating with webapi.py
  function getAccounts() {
    fetch("http://localhost:8000/getAccounts")
      .then((d) => d.json())
      .then((d) => {
        console.log(d);
        accounts = new Map();
        for (const key in d) {
          accounts.set(key, d[key]);
        }
        console.log(accounts);
      });
  }

  let inCharging = [];
  function getInCharging() {
    fetch("http://localhost:8000/inCharging")
      .then((d) => d.json())
      .then((d) => (inCharging = d));
  }

  function getBalance(userId) {
    fetch(`http://localhost:8000/balance/${userId}`)
      .then((d) => d.json())
      .then((d) => {
        console.log(d);
        let account = accounts.get(userId);
        account.balance = d;
        accounts.set(userId, account);
        accounts = accounts;
      });
  }

  function createAccount(userId) {
    console.log("creating account");
    fetch(`http://localhost:8000/createAccount/${userId}`)
      .then(handleErrors)
      .catch((e) => {
        console.log(e);
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
    console.log(userId, chargerId, estimatedDuration, desiredkWh, offeredFlex);
    fetch(
      `http://localhost:8000/startCharging/${userId}/${chargerId}/${estimatedDuration.toFixed(
        0
      )}/${desiredkWh}/${offeredFlex}`
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

  // charger IDs
  let knownChargers = [
    "AG-1F01",
    "AG-1F02",
    "AG-1F03",
    "AG-1F04",
    "AG-1F05",
    "AG-1F06",
    "AG-1F07",
    "AG-1F08",
    "AG-1F09",
    "AG-1F10",
    "AG-1F11",
    "AG-1F12",
    "AG-1F13",
    "AG-1F14",
    "AG-3F15",
    "AG-3F16",
    "AG-3F17",
    "AG-3F18",
    "AG-3F19",
    "AG-3F20",
    "AG-3F21",
    "AG-3F22",
    "AG-3F23",
    "AG-3F24",
    "AG-3F25",
    "AG-3F26",
    "AG-3F27",
    "AG-3F28",
    "AG-3F29",
    "AG-3F30",
    "AG-3F31",
    "AG-3F32",
    "AG-3F33",
    "AG-4F34",
    "AG-4F35",
    "AG-4F36",
    "AG-4F37",
    "AG-4F38",
    "AG-4F39",
    "AG-4F39",
    "AG-4F40",
    "AG-4F41",
    "AG-4F42",
    "AG-4F43",
    "AG-4F44",
    "AG-4F45",
    "AG-4F46",
    "AG-4F47",
    "AG-4F48",
    "AG-4F49",
    "AG-4F50",
    "AG-4F51",
    "AG-4F52",
  ];

  //-----------------------------------------------

  let clicked = 0;

  onMount(async () => {
    getInCharging();
    getAccounts();
  });


  let selectedAccountId = "Stephen Hawking";
  let selectionIndex = null;
  let selectedChargerId;
</script>

<!-- CSS section -->
<style>
  :global(html) {
    margin:0;
    height: 100%;
    font-family: Arial, Helvetica, sans-serif;
  }
  :global(body) {
    margin:0;
    min-height: 100vh;
    font-family: Arial, Helvetica, sans-serif;
  }
  * :global(.card-media-16x9) {
    background-image: url(https://via.placeholder.com/320x180.png?text=16x9);
  }
  * :global(.card-media-square) {
    background-image: url(https://via.placeholder.com/320x320.png?text=square);
  }

  .content-row {
    display: flex;
  }

  * :global(.mdc-select) {
    width: 100%;
    margin-bottom: 5px;
  }

  @media (max-width: 1280px) {
    .content-row {
      flex-direction: column;
    }
  }

  .content-column-left {
    flex: 100%;
    overflow: auto;
    border-bottom: 1px #ccc solid;
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
      border-bottom: 0px #ccc solid;
      border-right: 1px #ccc solid;
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

<!-- HTML section -->
<div class="header">
  <h2 style="margin-left: 18px;">Charging Processes</h2>
  <div class="menu-bar">
    <Meta class="material-icons" style="font-size:40px; cursor:pointer" on:click={getInCharging}>refresh</Meta>
  </div>
</div>

<div
  class="content-row"
  style="border:1px #ccc solid;margin:10px;border-radius:15px;height: calc(100vh - 90px);">
  <div class="content-column-left">
    <div
      style="display: flex;justify-content: space-between;border-bottom:1px #ccc solid;">
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
          <Meta
            style="font-size: 40px;"
            class="material-icons"
            on:click={sliderDialog.open()}>
            electrical_services
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
            <span slot="label">Flex to Boost</span>
          </FormField>
        </div>
      </Content>
      <Actions>
        <Button
          action="accept"
          on:click={() => {
            startCharging(selectedAccountId, selectedChargerId, estimatedDuration, desiredkWh, offeredFlex);
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
  <div
    class="content-column-right"
    style="display: flex; flex-wrap: wrap; margin-bottom: auto; margin-bottom: auto;">
    {#each inCharging as chargingProcess, i}
      <Card style="width: 400px;margin: 10px;background-color: #f0f0f0; margin-bottom:auto;">
        <PrimaryAction on:click={() => clicked++}>
          <Content class="mdc-typography--body2">
            <h2 class="mdc-typography--headline6" style="margin: 0;">
              Charging Process No.
              {i}
            </h2>
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
                  <td style="text-align:right">{chargingProcess.userID}</td>
                </tr>
                <tr>
                  <td><strong>Station ID:</strong></td>
                  <td style="text-align:right">{chargingProcess.chargerID}</td>
                </tr>
                <tr>
                  <td><strong>Charging Time:</strong></td>
                  <td style="text-align:right">
                    {chargingProcess.estimatedDuration / 3600} h 
                  </td>
                </tr>
                <tr>
                  <td><strong>Flexibility offered:</strong></td>
                  <td style="text-align:right">
                    {chargingProcess.availableFlex / 1e18 } Ether
                  </td>
                </tr>
              </tbody>
            </table>
          </Content>
        </PrimaryAction>
        <div class="action-buttons">
          <Actions>
            <ActionButtons>
              <Button
                on:click={() => {
                  selectedAccountId = chargingProcess.userID;
                  selectedChargerId = chargingProcess.chargerID;
                  selectedAvailableFlex = chargingProcess.availableFlex / 1e18;
                  sliderDialogStop.open();
                }}>
                <Meta style="font-size: 40px;" class="material-icons">
                  power_off
                </Meta>
              </Button>
            </ActionButtons>
          </Actions>
        </div>
      </Card>
    {/each}
  </div>
  <Dialog
    bind:this={sliderDialogStop}
    aria-labelledby="slider-title"
    aria-describedby="slider-content">
    <Title id="slider-title">Stop Charging</Title>
    <Content id="slider-content">
      <div>
        <FormField align="end" style="display: flex; flex-direction: column;">
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
        <FormField align="end" style="display: flex; flex-direction: column;">
          <Slider
            bind:value={flexFlow}
            min={0}
            max={selectedAvailableFlex}
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
          stopCharging(selectedAccountId, selectedChargerId, flexFlow, chargedkWh);
          sliderDialogStop.close();
          getInCharging();
        }}>
        <Label>Stop</Label>
      </Button>
      <Button action="cancel" on:click={sliderDialogStop.close()}>
        <Label>Cancel</Label>
      </Button>
    </Actions>
  </Dialog>
</div>
