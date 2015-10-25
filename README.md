Subscriptions for RequestPolicy
=============

Subscriptions for the [RequestPolicyContinued](https://requestpolicycontinued.github.io/) Firefox addon.

Subscriptions are preset rules for RequestPolicy Continued. Subscriptions are configurable through the `Preferences -> Manage Policies -> Subscriptions` menu of the addon.

Enabling a subscription will load a preconfigured allow/deny policy for certain sites. For example, subscriptions can:
 * Block some known web tracking services.
 * Allow certain sites to work properly (allow them to request some required elements form other domains)
 

-------------------------------------------

## What is included in subscriptions
You can check what requests are affected by different subscriptions by manually inspecting the subscription files. On your computer, RequestPolicy downloads subscriptions to the following locations:

 * Linux: `~/.mozilla/firefox/$profile_dir/requestpolicy/policies/subscriptions/`
 * Windows: `C:\Users\%USERNAME\AppData\Roaming\Mozilla\Firefox\Profiles\%PROFILE_DIR\requestpolicy\policies\subscriptions\`

See [How to read subscriptions files](#how-to-read-subscriptions-files) for information on the file format.

-------------------------------------------

## Contributing
If you have a question or remark about how RequestPolicy Continued handles subscriptions, check the [main project issue tracker](https://github.com/RequestPolicyContinued/requestpolicy/labels/subscriptions).

If you'd like a rule to be **removed** from the subscriptions, please file a new [issue](https://github.com/RequestPolicyContinued/subscriptions/issues/) stating the reason why it should be removed.

If you want your rules **added** to the official subscriptions, please mind the following:

 * [Create a blank Firefox profile](https://support.mozilla.org/en-US/kb/profile-manager-create-and-remove-firefox-profiles), with only RequestPolicy Continued installed.
 * In your RequestPolicy preferences, enable the subscription you want to work on to avoid duplicating already established rules.
 * **Allow rules should be kept to a minimum** (no pretty fonts, no tracking scripts, no ad networks, no optional sharing widgets...)
 * Do not reorder/sort existing rules. (Rules that affect a particular site should stay grouped, and this helps reviewing your changes). 
 * Check for duplicate rules (eg. `egrep -ho '\{.*\}' *.json | sort | uniq -d`), check JSON validity (http://jsonlint.com/) before doing a pull request.
 * Read this README


#### Adding rules
You can also help by adding your rules for sites you like:

 * [Fork](https://github.com/RequestPolicyContinued/subscriptions/fork) this repository.
 * Visit your favorite sites, one by one. You can also work on top websites from http://www.alexa.com/topsites/countries
 * For each site, check if a blocked domain causes basic display/functionality breakage.

 * Copy rules from your `policies/user.json` in your firefox profile directory to `official_allow-functionality.json` in your copy of the subscriptions repository, one rule per line.
  * `user.json` stores all rules on a single line ([issue 339](https://github.com/RequestPolicyContinued/requestpolicy/issues/339)). To convert your rules to the one-rule-per-line format used in subscriptions, replace `}},` with `}},\n` in your file. This helps copying rules to the subscription file.
 * When done, commit your changes and submit a Pull Request with a proper description so that it can be reviewed.


#### Adding rules to allow_sameorg.json
It is easier to add all rules in `official_allow-functionality.json` first. You can also help by adding rules to `official_allow-sameorg.json`, either directly, or by moving already existing rules from `official_allow-functionality.json`. In this case:

   * check this domain owner info using WHOIS
   * if the destination domain owner matches the origin owner, add a rule for this origin->destination pair at the end of `official-allow_sameorg.json` (If the subscription grows too large in the future, it will be split - [#1](https://github.com/RequestPolicyContinued/subscriptions/issues/1))
   * if owners/organizations/companies don't match, but the request is still required for the website to work properly, the rule should remain in `official-allow_functionality.json`


#### Tips

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

```

#### Improving the _deny trackers_ list

Additions to the _deny trackers_ list are also welcome.

#### Translating subscriptions titles and descriptions
Look at `locale.json` and feel free to add the translations for subscriptions titles and language there.


--------------------------------------------------------------------------------

## How to read subscriptions files
RequestPolicy Continued fetches available subscriptions from **subscription lists**. [official.json](official.json) is the default subscription list (the only list currently) Each **subscription list** lists several **subscriptions**, which contain the actual rules.



The **subscriptions lists** file format is the following (eg. `official.json`):

```
{
  "subscriptions":{ 
    "allow_embedded":{ <- short name of the subscription.
      "serial":1329159661, <- a serial number; RP compares your local file serial number to the one available online, and updates your file if it has a lower serial.
      "url":"https://raw.githubusercontent.com/RequestPolicyContinued/subscriptions/master/official-allow_embedded.json", <- the URL from which up-to-date subscription rules should be downloaded
      "title":"Your title here", <- the title of this subscription
      "description":"This subscription does this." <- a description of what purpose this subscription serves, how it works
      },
    "another_subscription_here": { ...
```

`locale.json` contains translations for each subscription's list and title.


The **subscription** file format is the following (eg. `official-allow_functionality.json`):

```
{
  "metadata":{
    "version":1,
    "serial":1334341442 <- a serial number; RP compares your local file serial number to the one available online, and updates your file if it has a lower serial.
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

For each rule, `"o:"{"h":"*.hostname.org"}` is the origin host for the request, `"d":{"h":"*.another.com"}` is the destination host for this request. What action is applied to this particular requests depends on which section it is listed in (`"allow":[` or `"deny":[`)