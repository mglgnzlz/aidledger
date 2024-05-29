App = {
  loading: false,
  contracts: {},
  load: async () => {
    console.log("App loading...");
    await App.loadWeb3();
    await App.loadAccount();
    await App.loadContract();
    await App.render();
    await App.renderReliefGoods();
  },
  // Load Web3
  loadWeb3: async () => {
    if (typeof web3 !== "undefined") {
      App.web3Provider = window.ethereum;
      web3 = new Web3(window.ethereum);
    } else {
      window.alert("Please connect to Metamask.");
    }
    // Modern dapp browsers...
    if (window.ethereum) {
      window.web3 = new Web3(ethereum);
      try {
        // Request account access if needed
        await ethereum.request({ method: "eth_requestAccounts" });
        // Acccounts now exposed
        web3.eth.sendTransaction({
          /* ... */
        });
      } catch (error) {
        // User denied account access...
      }
    }
    // Legacy dapp browsers...
    else if (window.web3) {
      App.web3Provider = window.ethereum;
      window.web3 = new Web3(window.ethereum);
      // Acccounts always exposed
      web3.eth.sendTransaction({
        /* ... */
      });
    }
    // Non-dapp browsers...
    else {
      console.log(
        "Non-Ethereum browser detected. You should consider trying MetaMask!"
      );
    }
  },
  // Load account
  loadAccount: async () => {
    App.account = web3.eth.accounts[0];
    console.log("Account: ", App.account);
  },
  // Load contract
  loadContract: async () => {
    const aidLedger = await $.getJSON("AidLedger.json");
    App.contracts.AidLedger = TruffleContract(aidLedger);
    App.contracts.AidLedger.setProvider(App.web3Provider);
    console.log("Contract: ", aidLedger);

    App.aidLedger = await App.contracts.AidLedger.deployed();
  },
  render: async () => {
    // Prevent double rendering
    if (App.loading) {
      return;
    }

    // Update loading state to true
    App.setLoading(true);

    // Render account
    $("#account").html(App.account);

    // Update loading state to false
    App.setLoading(false);
  },
  renderReliefGoods: async () => {
    // Load total relief goods count from the blockchain
    const reliefGoodCount = await App.aidLedger.reliefGoodCount();
    const $reliefGoodTemplate = $(".reliefGoodTemplate");
    console.log("Relief good count: ", reliefGoodCount.toNumber());

    // Render each relief good with new relief good template
    for (var i = 1; i <= reliefGoodCount; i++) {
      const reliefGood = await App.aidLedger.reliefGoods(i);
      const reliefGoodId = reliefGood[0].toNumber();
      const reliefGoodDonor = reliefGood[1];
      const reliefGoodDescription = reliefGood[2];
      const reliefGoodStatus = reliefGood[3];
      const reliefGoodRecipient = reliefGood[4];
      console.log(reliefGood);

      // Create the html for the relief good
      const $newReliefGoodTemplate = $reliefGoodTemplate.clone();
      $newReliefGoodTemplate.find(".id").html(reliefGoodId);
      $newReliefGoodTemplate.find(".donor").html(reliefGoodDonor);
      $newReliefGoodTemplate.find(".description").html(reliefGoodDescription);
      $newReliefGoodTemplate.find(".status").html(reliefGoodStatus);
      $newReliefGoodTemplate.find(".recipient").html(reliefGoodRecipient);

      $("#reliefGoodList").append($newReliefGoodTemplate);

      // Show relief goods
      $newReliefGoodTemplate.show();
    }
  },

  setLoading: (boolean) => {
    App.loading = boolean;
    const loader = $("#loader");
    const content = $("#content");
    if (boolean) {
      loader.show();
      content.hide();
    } else {
      loader.hide();
      content.show();
    }
  },
};

$(() => {
  $(window).load(() => {
    App.load();
  });
});
