Subscriptions for RequestPolicy
=============

Subscriptions for the [RequestPolicyContinued](https://requestpolicycontinued.github.io/) Firefox addon.

Subscriptions are preset rules for RequestPolicy Continued. Subscriptions are configurable through the `Preferences -> Manage Policies -> Subscriptions` menu of the addon.
Enabling a subscription will load a preconfigured allow/deny policy for certain sites. For example, subscriptions can:
 * Block some known web tracking services.
 * Allow certain sites to work properly (allow them to request some required elements form other domains)
 

## How subscriptions work
The default available subscriptions are:


#### [allow_sameorg](official-allow_sameorg.json) - Allow destinations that belong to the same organization as the origin webpage

Contains only rules absolutely for the website's core functionality to work.
 
Examples: a shopping website should allow shopping, a voting website should allow voting, a videos website should allow watching videos, a file hosting website should allow usual operations with files...
 
If the destination is not the **same organization, person, or company** as the origin, the rule does not qualify for `official-allow_sameorg.json`. If it is still absolutely necessary for the site to work properly, it is added to `official-allow_functionality.json`
   
#### [allow_functionality](official-allow_functionality.json) - Allow requests that are needed for websites to work properly

Contains only rules absolutely for the website to work, but that do not qualify for `official-allow_sameorg.json`
 
Functionality that is not a core part of the site (comment systems, sharing via external services...) should not be included. 


#### [deny_trackers](official-deny_trackers.json) - Blocks some websites known for tracking your web browsing habits

This contains a list of websites that are known for tracking your browsing across the web. This is mainly useful to provide a minima security/privacy when using the _Allow all requests by default_ default policy.

#### [allow_embedded](official-allow_embedded.json) - Allow requests for embedded content such as images and videos

**Broken.** Suggested solution: Drop this subscription.

 * Implement _"bundles"_ in RequestPolicy (_"groups"?_) for different content types (fonts, videos, maps, CDNs...), depends on https://github.com/RequestPolicyContinued/requestpolicy/issues/338 and https://github.com/RequestPolicyContinued/requestpolicy/issues/166#issuecomment-65426226.
  * This will add the ability to whitelist/blacklist whole groups from the menu.
   * Examples: `Allow requests to **Videos** group`, `Allow requests to **Videos** group from *.thisdomain.com`
  * If really necessary, these bundles will be added as new subscriptions.
   * The only benefit is the ability to allow requests for these bundles during initial setup. Otherwise users will just have to `Allow requests to **Videos** group` the first time they are blocked.


---------------------------------

## What is included in subscriptions
You can check what requests are affected by different subscriptions by manually inspecting the files mentioned above. On your computer, RequestPolicy downloads subscriptions to the following locations:

 * Linux: `~/.mozilla/firefox/$profile_dir/requestpolicy/policies/subscriptions/`
 * Windows: `C:\Users\%USERNAME\AppData\Roaming\Mozilla\Firefox\Profiles\%PROFILE_DIR\requestpolicy\policies\subscriptions\`


See [How to read subscriptions files](#how-to-read-subscriptions-files) for information on the file format.

-------------------------------------------

## Contributing

#### Country-specific allow lists

The next step is to **add rules for top sites for specific countries**. Workflow:

   * Read this README
   * Pick a country you want to work on and report it as a [new issue](https://github.com/RequestPolicyContinued/subscriptions/issues/new)
   * Grab traffic data from http://www.alexa.com/topsites/countries
   * Create a new, blank firefox profile with only RequestPolicy enabled.
   * In the preferences, enable the subscription you want to work on to avoid duplicating already established rules.
   * Fork this repository on github, and open `json` files on your fork and start editing
   * Visit each listed domain, one by one. For each:
     * check if a blocked domain causes basic display/functionality breakage.
     * check this domain owner info using WHOIS
     * if the destination domain owner matches the origin owner, add a rule for this origin->destination pair at the end of `official-allow_sameorg.json` (If the subscription grows too large in the future, it will be split - [#1](https://github.com/RequestPolicyContinued/subscriptions/issues/1))
     * if owners/organizations/companies don't match, but the request is still required for the website to work properly, add the rule to `official-allow_functionality.json`
   * Do not reorder/sort existing rules. (Rules that affect a particular site should stay grouped). Check for duplicate rules (`sort official-allow_sameorg.json |uniq -c`), check JSON validity (http://jsonlint.com/).
   * When you think you're done, commit your changes and submit a Pull Request with a proper description so that it can be reviewed.


A few bash tricks that may help reviewing/building subscriptions:

```
function wh() { #get relevant info about domain owners
  whois "$1" | grep -i registrant
}

function rprule() {
        #generate a rule with proper syntax for inclusion in subscriptions, copy it to clipboard
        # usage: rprule [origin-domain] [destination-domain]
  echo "{\"o\":{\"h\":\"*.$1\"},\"d\":{\"h\":\"*.$2\"}}," | xclip -selection c
}

 |sort #check for duplicates in file
```

#### Improving the _deny trackers_ list

Additions to the _deny trackers_ list are welcome.


#### Questions/additions/removal requests

If you think a rule should be added/removed from official subscriptions, let us know in the [issues tracker](https://github.com/RequestPolicyContinued/subscriptions/issues) of this repository.
If you have a question or remark about how RequestPolicy Continued handles subscriptions, check the [main project issue tracker](https://github.com/RequestPolicyContinued/requestpolicy/labels/subscriptions).

--------------------------------------------------------------------------------

#### How to read subscriptions files
RequestPolicy Continued fetches available subscriptions from **subscription lists**. [official.json](official.json) is the default subscription list (the only list currently) Each **subscription list** lists several **subscriptions**.



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