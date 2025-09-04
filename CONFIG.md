# 🎯 Bot Configuration Guide

**⚠️ YOU MUST CONFIGURE THIS BEFORE RUNNING THE BOT!**

The bot comes pre-configured for someone selling Bitcoin, but you need to adjust it for your strategy.

## 🔧 Step-by-Step Setup

### **Step 1: Determine Your Strategy**

**Are you primarily:**
- 🟢 **Selling Bitcoin?** → You want alerts for **#BUYCOP** (buyers)
- 🔵 **Buying Bitcoin?** → You want alerts for **#SELLCOP** (sellers)  
- 🟡 **Both?** → You want alerts for **#BUYCOP** and **#SELLCOP**

### **Step 2: Edit config.json**

Open the `config.json` file and replace the entire `filters` section with one of these:

---

## 🟢 **For SELLING Bitcoin (Current Default)**

**You want:** Buyers offering good rates (market rate or premium)

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
  }
}
```

**What this does:**
- ✅ Shows buyers offering: `yadio.io -1%`, `yadio.io 0%`, `yadio.io +1%`, `yadio.io +5%`, etc.
- ❌ Hides buyers offering: `yadio.io -2%`, `yadio.io -5%` (too low for you)
- ❌ Ignores all #SELLCOP messages

**Adjust the rate:** Change `-1.0` to your minimum acceptable rate (e.g., `-0.5` for stricter filtering)

---

## 🔵 **For BUYING Bitcoin**

**You want:** Sellers offering good rates (market rate or discount)

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
  }
}
```

**What this does:**
- ✅ Shows sellers offering: `yadio.io +1%`, `yadio.io 0%`, `yadio.io -1%`, `yadio.io -5%`, etc.
- ❌ Hides sellers offering: `yadio.io +2%`, `yadio.io +5%` (too expensive for you)  
- ❌ Ignores all #BUYCOP messages

**Adjust the rate:** Change `1.0` to your maximum acceptable rate (e.g., `0.5` for stricter filtering)

---

## 🟡 **For BOTH Buying and Selling**

**You want:** Both buyers and sellers with good rates

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
  }
}
```

**What this does:**
- ✅ Shows buyers offering -1% or better (for when you want to sell)
- ✅ Shows sellers offering +1% or better (for when you want to buy)
- ❌ Filters out bad rates on both sides

---

## 📊 **Understanding the Numbers**

### **For #BUYCOP (Buyers):**
- `"min_percentage": -1.0` = Reject buyers offering worse than -1%
- `"max_percentage": null` = Accept any premium (no upper limit)

### **For #SELLCOP (Sellers):**
- `"min_percentage": null` = Accept any discount (no lower limit)  
- `"max_percentage": 1.0` = Reject sellers charging more than +1%

### **Special Values:**
- `null` = No limit (unlimited)
- `-1.0` = Negative 1% (discount from market)
- `1.0` = Positive 1% (premium above market)
- `0.0` = Exactly market rate

---

## 🔄 **After Making Changes**

1. **Save** the `config.json` file
2. **Restart** your bot (stop and run again)
3. **Check** the console for any config errors
4. **Test** with a few messages to make sure it's working

---

## 🎯 **Real Examples**

### **Conservative Seller (strict rates):**
```json
"#BUYCOP": {
  "min_percentage": -0.5,
  "max_percentage": null
}
```
*Only accepts buyers offering -0.5% or better*

### **Aggressive Buyer (will pay premium):**
```json
"#SELLCOP": {
  "min_percentage": null,
  "max_percentage": 2.0
}
```
*Accepts sellers charging up to +2% premium*

### **Market Rate Only:**
```json
"#BUYCOP": {
  "min_percentage": -0.1,
  "max_percentage": 0.1
}
```
*Only accepts rates very close to market (±0.1%)*

---

## ❓ **Common Questions**

**Q: Why am I getting no alerts?**
A: Your rates might be too strict. Try increasing the range (e.g., change `-1.0` to `-2.0`)

**Q: Getting too many alerts?**  
A: Make your rates stricter (e.g., change `-1.0` to `-0.5`)

**Q: Want different rate providers?**
A: Change `"yadio.io"` to `"binance.com"` or add multiple providers

**Q: Bot stopped working after config change?**
A: Check your JSON syntax - use an online JSON validator if needed

### Current Configuration:
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

### **How It Works (Much Simpler!):**

**#BUYCOP (Looking for Buyers - you're selling):**
- `min_percentage: -1.0` = Won't accept buyers offering worse than -1%
- `max_percentage: null` = No upper limit (higher premiums welcomed!)
- **Logic:** Buyers offering -1%, 0%, +1%, +5%, +10%+ all accepted

**#SELLCOP (Looking for Sellers - you're buying):**
- `min_percentage: null` = No lower limit (bigger discounts welcomed!)
- `max_percentage: 1.0` = Won't accept sellers charging more than +1%
- **Logic:** Sellers offering -10%, -5%, 0%, +1% all accepted

### **Key Benefits:**
- **No confusing inversion logic** - each order type has direct settings
- **Intuitive limits** - set exactly what you want for each scenario
- **Easy to modify** - change one value to adjust your strategy

## 🔧 Configuration Options

### **Hashtag Filtering** (`filters.hashtags`):
- `["#BUYCOP"]` - Only buy orders
- `["#SELLCOP"]` - Only sell orders  
- `["#BUYCOP", "#SELLCOP"]` - Both buy and sell orders

### **Rate Providers** (`filters.rate_providers`):
- `["yadio.io"]` - Only yadio.io rates
- `["yadio.io", "binance.com"]` - Multiple providers
- `["coinbase.com"]` - Different provider

### **Rate Thresholds** (`filters.rate_thresholds`):
- **yadio.io alone** (no percentage) = 0% (market rate)
- **yadio.io +1%** = 1% above market  
- **yadio.io -1%** = 1% below market
- Configure min/max range for each provider

### **Message Formatting** (`formatting`):
- `buy_prefix` - Text shown for buy orders
- `sell_prefix` - Text shown for sell orders
- `rate_prefix` - Text shown before rate
- `separator` - Line between content and link
- `link_text` - Text for the clickable link

## 📝 Example Configurations

### **Only Looking for Buyers (selling Bitcoin):**
```json
{
  "filters": {
    "hashtags": ["#BUYCOP"],
    "rate_providers": ["yadio.io"],
    "rate_thresholds": {
      "yadio.io": {
        "#BUYCOP": {
          "min_percentage": -0.5,
          "max_percentage": null
        }
      }
    }
  }
}
```
*Accepts buyers offering -0.5%, 0%, +1%, +10%+ (no upper limit)*

### **Only Looking for Sellers (buying Bitcoin):**
```json
{
  "filters": {
    "hashtags": ["#SELLCOP"],
    "rate_providers": ["yadio.io"],
    "rate_thresholds": {
      "yadio.io": {
        "#SELLCOP": {
          "min_percentage": null,
          "max_percentage": 0.5
        }
      }
    }
  }
}
```
*Accepts sellers offering -10%, -1%, 0%, +0.5% (no lower limit)*

### **Very Strict Market Rates Only:**
```json
{
  "filters": {
    "hashtags": ["#BUYCOP", "#SELLCOP"],
    "rate_providers": ["yadio.io"],
    "rate_thresholds": {
      "yadio.io": {
        "#BUYCOP": {
          "min_percentage": 0.0,
          "max_percentage": 0.5
        },
        "#SELLCOP": {
          "min_percentage": -0.5,
          "max_percentage": 0.0
        }
      }
    }
  }
}
```
*Very strict: Only accepts rates very close to market*

### **Multiple Rate Providers**:
```json
{
  "filters": {
    "hashtags": ["#BUYCOP", "#SELLCOP"],
    "rate_providers": ["yadio.io", "binance.com", "coinbase.com"],
    "rate_thresholds": {
      "yadio.io": {"min_percentage": -1.0, "max_percentage": 1.0},
      "binance.com": {"min_percentage": -0.5, "max_percentage": 0.5},
      "coinbase.com": {"min_percentage": -2.0, "max_percentage": 2.0}
    }
  }
}
```

## 🔄 Updating Configuration

1. **Edit `config.json`**
2. **Restart the bot** - configuration is loaded on startup
3. **Check console** for any config errors

## ⚠️ Important Notes

- **yadio.io** (no percentage) = assumes 0% market rate
- **Invalid JSON** = bot falls back to default settings
- **Missing file** = bot uses built-in defaults
- **Rate ranges** = inclusive (min_percentage ≤ rate ≤ max_percentage)
