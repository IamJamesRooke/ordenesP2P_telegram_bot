# Configuration Templates

Copy one of these complete configurations into your `config.json` file:

## Template 1: Selling Bitcoin (Looking for Buyers)
```json
{
  "filters": {
    "hashtags": ["#BUYCOP"],
    "rate_providers": ["yadio.io"],
    "rate_thresholds": {
      "yadio.io": {
        "#BUYCOP": {
          "min_percentage": -1.0,
          "max_percentage": null
        }
      }
    }
  },
  "formatting": {
    "buy_prefix": "*Buyer Found:*",
    "sell_prefix": "*Seller Found:*",
    "rate_prefix": "*Rate:*",
    "separator": "————————————",
    "link_text": "📱 View Offer"
  }
}
```

## Template 2: Buying Bitcoin (Looking for Sellers)
```json
{
  "filters": {
    "hashtags": ["#SELLCOP"],
    "rate_providers": ["yadio.io"],
    "rate_thresholds": {
      "yadio.io": {
        "#SELLCOP": {
          "min_percentage": null,
          "max_percentage": 1.0
        }
      }
    }
  },
  "formatting": {
    "buy_prefix": "*Buyer Found:*",
    "sell_prefix": "*Seller Found:*",
    "rate_prefix": "*Rate:*",
    "separator": "————————————",
    "link_text": "📱 View Offer"
  }
}
```

## Template 3: Both Buying and Selling
```json
{
  "filters": {
    "hashtags": ["#BUYCOP", "#SELLCOP"],
    "rate_providers": ["yadio.io"],
    "rate_thresholds": {
      "yadio.io": {
        "#BUYCOP": {
          "min_percentage": -1.0,
          "max_percentage": null
        },
        "#SELLCOP": {
          "min_percentage": null,
          "max_percentage": 1.0
        }
      }
    }
  },
  "formatting": {
    "buy_prefix": "*Buyer Found:*",
    "sell_prefix": "*Seller Found:*",
    "rate_prefix": "*Rate:*",
    "separator": "————————————",
    "link_text": "📱 View Offer"
  }
}
```

## How to Use:
1. Choose the template that matches your strategy
2. Copy the entire JSON block
3. Replace the contents of your `config.json` file
4. Modify the percentage values if needed
5. Restart the bot
