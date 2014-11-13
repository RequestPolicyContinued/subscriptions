subscriptions
=============

Subscriptions for the [RequestPolicyContinued](https://requestpolicycontinued.github.io/) Firefox addon.

Subscriptions are preset rules for RequestPolicy Continued. Subscriptions are configurable through the `Preferences -> Manage Policies -> Subscriptions` menu of the addon.
Enabling a subscription will load a preconfigured allow/deny policy for certain sites. For example, subscriptions can:
 * Block some known web tracking services.
 * Allow certain sites to work properly by allowing them to request required elements from other domains (Content Delivery Networks..).
 
Currently this repository only contains the _official_ subscriptions, copied from the original project on requestpolicy.com.

## Contributing
If you think a rule should be added to official subscriptions, of if you would like to submit your own subscription list, let us know in the [issues tracker](https://github.com/RequestPolicyContinued/subscriptions/issues) of this repository.
If you have a question or remark about how RequestPolicy Continued handles subscriptions, check the [main project issue tracker](https://github.com/RequestPolicyCOntinued/requestpolicy/issues).


## How subscriptions work
RequestPolicy Continued fetches avalable subscriptions from **subscription lists**. Each **subscription list** is a [JSON](https://en.wikipedia.org/wiki/JSON) file that lists several **subscriptions** you are given the choice to enable from the addons [Subscriptions preferences page](chrome://requestpolicy/content/settings/subscriptions.html). 


## Default subscriptions
[official.json](official.json) is the default subscription list. You can enable the following subscriptions that are listed in this file:
 * [official-allow_embedded.json](official-allow_embedded.json) - Allow requests for embedded content such as images and videos
 * [official-allow_sameorg.json](official-allow_sameorg.json) -  Allow destinations that belong to the same organization as the origin webpage
 * [official-deny_trackers.json](official-deny_trackers.json) - Blocks some websites known for tracking your web browsing habits.

 
## What is included in subscriptions
You can check what requests are affected by different subscriptions by manually inspecting the files mentioned above. On your computer, RequestPolicy downloads subscriptions to the following locations:

 * Linux: `~/.mozilla/firefox/$profile_dir/requestpolicy/policies/subscriptions/`
 * Windows: `C:\Users\%USERNAME\AppData\Roaming\Mozilla\Firefox\Profiles\%PROFILE_DIR\requestpolicy\policies\subscriptions\`
 
### How to read subscriptions files
The subscriptions **lists** file format is the following:

```
{
  "subscriptions":{ 
    "allow_embedded":{ <- short name of the subscription.
      "serial":1329159661, <- a serial number; RP compares your local file serial number to the one available online, and updates you file if it has a lower serial.
      "url":"https://raw.githubusercontent.com/RequestPolicyContinued/subscriptions/master/official-allow_embedded.json" <- the URL from which the new subscriptions should be downloaded
      },
    "another_subscription_here": { ...
```

The subscription file format is the following:

```
{
  "metadata":{
    "version":1,
    "serial":1334341442 <- a serial number; RP compares your local file serial number to the one available online, and updates you file if it has a lower serial.
  },
  "entries":{ <- this marks the begginning of the actual subscription rules
    "allow":[ <- rules in this section are requests that will be **allowed** by RequestPolicy
      {"o":{"h":"*.amazon.ca"},"d":{"h":"*.images-amazon.com"}},
      {"o":{"h":"*.amazon.ca"},"d":{"h":"*.ssl-images-amazon.com"}},
      {"o":{"h":"*.amazon.com"},"d":{"h":"*.amazonaws.com"}}
    ],
    "deny":[] <- rules in this section are requests that will be **denied** by RequestPolicy
  }
}
```

For each rule, `"o:"{"h":"*.hostname.org"}` is the **o**rigin **h**ost for the request, `"d":{"h":"*.another.com"}` is the **d**estination **h**ost for this request. What action is applied to this particular requests depends on which section it is listed in (`"allow":[` or `"deny":[`)
