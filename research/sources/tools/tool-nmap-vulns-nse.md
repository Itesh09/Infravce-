<div id="nst-wrapper">

<div id="menu">

<div class="blur">

<div id="nst-head">

<a href="#menu" id="menu-open" aria-label="Open menu"><img src="/shared/images/nst-icons.svg#menu" aria-hidden="true" width="44" height="44" /></a> <a href="#" id="menu-close" aria-label="Close menu"><img src="/shared/images/nst-icons.svg#close" aria-hidden="true" width="44" height="44" /></a> <a href="/" id="nst-logo" aria-label="Home page"><img src="/images/sitelogo.png" srcset="/images/sitelogo.png, /images/sitelogo-2x.png 2x" onerror="this.onerror=null;this.srcset=this.src" width="168" height="90" alt="Home page logo" /></a>

<a href="https://nmap.org/" class="nlink">Nmap.org</a> <a href="https://npcap.com/" class="nlink">Npcap.com</a> <a href="https://seclists.org/" class="nlink">Seclists.org</a> <a href="https://sectools.org" class="nlink">Sectools.org</a> <a href="https://insecure.org/" class="nlink">Insecure.org</a>

<img src="/shared/images/nst-icons.svg#search" style="width:100%;aspect-ratio:1/1;" aria-hidden="true" />

</div>

</div>

</div>

<div id="nst-content" role="main">

<a href="/download.html" class="nlink">Download</a> <a href="/book/man.html" class="nlink">Reference Guide</a> <a href="/book/" class="nlink">Book</a> <a href="/docs.html" class="nlink">Docs</a> <a href="/zenmap/" class="nlink">Zenmap GUI</a> <a href="/movies/" class="nlink">In the Movies</a>

<div id="nse-main">

<div id="nse-nav-general">

<a href="../index.html" class="nav-head">NSEDoc</a>

- [NSEDoc Portal](../index.html)
- [NSE Documentation](/book/nse.html)
- [Nmap API](/book/nse-api.html)
- [NSE Tutorial](/book/nse-tutorial.html)

</div>

<div id="nse-nav-scripts">

<a href="../scripts/" class="nav-head">Scripts</a>

</div>

<div id="nse-nav-lib">

<a href="../lib/" class="nav-head">Libraries</a>

</div>

<div id="nse-nav-cat">

<a href="../categories/" class="nav-head">Categories</a>

- [auth](../categories/auth.html)
- [broadcast](../categories/broadcast.html)
- [brute](../categories/brute.html)
- [default](../categories/default.html)
- [discovery](../categories/discovery.html)
- [dos](../categories/dos.html)
- [exploit](../categories/exploit.html)
- [external](../categories/external.html)
- [fuzzer](../categories/fuzzer.html)
- [info](../categories/info.html)
- [intrusive](../categories/intrusive.html)
- [malware](../categories/malware.html)
- [safe](../categories/safe.html)
- [version](../categories/version.html)
- [vuln](../categories/vuln.html)

</div>

<div id="nse-content">

[Script Arguments](#script-args) [Functions](#functions)

# Library `vulns`

Functions for vulnerability management.

The vulnerabilities library may be used by scripts to report and store vulnerabilities in a common format.

Reported vulnerabilities information must be stored in tables. Each vulnerability must have its own state: `NOT_VULN`: The program was confirmed to be not vulnerable. `LIKELY_VULN`: The program is likely to be vulnerable, this can be the case when we do a simple version comparison. This state should cover possible false positive situations. `VULN`: The program was confirmed to be vulnerable. `EXPLOIT`: The program was confirmed to be vulnerable and was exploited successfully. The `VULN` state will be set automatically. `DoS`: The program was confirmed to be vulnerable to Denial of Service attack. The `VULN` state will be set automatically.

To match different vulnerability states, like the `VULN` and `EXPLOIT` states or the `VULN` and `DoS` states, one can use the bitwise operations.

Vulnerability table: --------------------

    local vuln_table = {
      title = "BSD ftpd Single Byte Buffer Overflow", -- mandatory field
      state = vulns.STATE.EXPLOIT, -- mandatory field
      -- Of course we must confirm the exploitation, otherwise just mark
      -- it vulns.STATE.VULN if the vulnerability was confirmed.
      -- states: 'NOT_VULN', 'LIKELY_VULN', 'VULN', 'DoS' and 'EXPLOIT'


      -- The following fields are all optional

      IDS = { -- Table of IDs
         --  ID Type     ID (must be a string)
             CVE       = 'CVE-2001-0053',
             BID       = '2124',
      },

      risk_factor = "High", -- 'High', 'Medium' or 'Low'
      scores = { -- A map of the different scores
         CVSS = "10.0",
         CVSSv2 = "...",
      },

      description = [[
    One-byte buffer overflow in BSD-based ftpd allows remote attackers
    to gain root privileges.]],

      dates = {
         disclosure = { year = 2000, month = 12, day = 18},
      },

      check_results = { -- A string or a list of strings
         -- This field can store the results of the vulnerability check.
         -- Did the server return anything ? some specialists can
         -- investigate this and decide if the program is vulnerable.
      },

      exploit_results = { -- A string or a list of strings
         -- This field can store the results of the exploitation.
      },

      extra_info = { -- A string or a list of strings
         -- This field can be used to store and shown any useful
         -- information about the vulnerability, server, etc.
      },

      references = { -- List of references
         'http://www.openbsd.org/advisories/ftpd_replydirname.txt',

          -- If some popular IDs like 'CVE' and 'OSVBD' are provided
          -- then their links will be automatically constructed.
      },
    }

The following examples illustrates how to use the library.

Examples for `portrule` and `hostrule` scripts:

     -- portrule and hostrule scripts must use the vulns.Report class
     -- to report vulnerabilities
     local vuln_table = {
      title = "BSD ftpd Single Byte Buffer Overflow", -- mandatory field
      references = { -- List of references
         'http://www.openbsd.org/advisories/ftpd_replydirname.txt',
      },
      ...
     }
     ...
     vuln_table.state = vulns.STATE.VULN
     local report = vulns.Report:new(SCRIPT_NAME, host, port)
     return report:make_output(vuln_table, ...)

     local vuln_table = {
      title = "BSD ftpd Single Byte Buffer Overflow", -- mandatory field
      references = { -- List of references
         'http://www.openbsd.org/advisories/ftpd_replydirname.txt',
      },
      ...
     }
     ...
     vuln_table.state = vulns.STATE.VULN
     local report = vulns.Report:new(SCRIPT_NAME, host, port)
     report:add(vuln_table, ...)
     return report:make_output()

Examples for `prerule` and `postrule` scripts:

     local FID -- my script FILTER ID

     prerule = function()
       FID = vulns.save_reports()
       if FID then
         return true
       end
       return false
     end

     postrule = function()
       if nmap.registry[SCRIPT_NAME] then
         FID = nmap.registry[SCRIPT_NAME].FID
         if vulns.get_ids(FID) then
           return true
         end
       end
       return false
     end

     prerule_action = function()
       nmap.registry[SCRIPT_NAME] = nmap.registry[SCRIPT_NAME] or {}
       nmap.registry[SCRIPT_NAME].FID = FID
       return nil
     end

     postrule_action = function()
       return vulns.make_output(FID) -- show all the vulnerabilities
     end

     local tactions = {
       prerule = prerule_action,
       postrule = postrule_action,
     }

     action = function(...) return tactions[SCRIPT_TYPE](...) end

Library debug messages:

- Level 2: show the `NOT VULNERABLE` entries.
- Level 3: show all the vulnerabilities that are saved into the registry.
- Level 5: show all the other debug messages (useful for debugging).

Note: Vulnerability tables are always re-constructed before they are saved in the registry. We do this to avoid using vulnerability tables that are referenced by other objects to let the Lua garbage-collector collect these last objects.

**Authors:**

- Djalal Harouni
- Henri Doreau

**Copyright** © Same as Nmap--See <https://nmap.org/book/man-legal.html>

**Source:** <https://svn.nmap.org/nmap/nselib/vulns.lua>

## Script Arguments

vulns.short  
If set, vulnerabilities will be output in short format, a single line consisting of the host's target name or IP, the state, and either the CVE ID or the title of the vulnerability. Does not affect XML output.

vulns.showall  
If set, the library will show and report all the registered vulnerabilities which includes the `NOT VULNERABLE` ones. By default the library will only report the `VULNERABLE` entries: `VULNERABLE`, `LIKELY VULNERABLE`, `VULNERABLE (DoS)` and `VULNERABLE (Exploitable)`. This argument affects the following functions: vulns.Report.make_output(): the default output function for portule/hostrule scripts. vulns.make_output(): the default output function for postrule scripts. vulns.format_vuln() and vulns.format_vuln_table() functions.

## Functions

[add](#add) (script_name, ..., vulnerabilities)  
Adds vulnerability tables into the vulnerability database (registry).

[add_ids](#add_ids) (fid, ..., FILTER, IDs)  
Add vulnerability IDs type to the vulnerability database associated with the `FILTER ID`.

[add_popular_id](#add_popular_id) (self, id_type, callback)  
Registers and associates a callback function with the popular ID vulnerability type to construct and return popular links automatically.

[add_vulns](#add_vulns) (self, ..., vulnerabilities)  
Adds vulnerability tables to the report.

[find](#find) (fid, selection_filter, FILTER, selection)  
Search and return vulnerabilities in a list.

[find_by_id](#find_by_id) (fid, vuln_id_type, id, FILTER)  
Search vulnerability entries by ID and return the results in a list.

[format_vuln](#format_vuln) (vuln_table, showall)  
Format the vulnerability information and return it as a string.

[format_vuln_table](#format_vuln_table) (vuln_table, showall)  
Format the vulnerability information and return it in a table.

[get_ids](#get_ids) (fid, FILTER)  
Gets the vulnerability database associated with the `FILTER ID`.

[get_popular_link](#get_popular_link) (id_type, id)  
Calls the function associated with the popular ID vulnerability type to construct and to return the appropriate reference link.

[lookup_id](#lookup_id) (fid, vuln_id_type, id, FILTER)  
Lookup for a vulnerability entry in the vulnerability database associated with the `FILTER ID`.

[make_output](#make_output) (self, ..., vulnerabilities)  
Report vulnerabilities.

[make_output](#make_output) (self, ..., vulnerabilities)  
Report vulnerabilities.

[new](#new) (self, script_name, host, port)  
Creates a new Report object

[register_popular_id](#register_popular_id) (id_type, callback)  
Registers and associates a callback function with the popular ID vulnerability type to construct and return popular links automatically.

[save_reports](#save_reports) (filter_callback)  
Initializes the vulnerability database and instructs the library to save all the vulnerability tables reported by scripts into this database (registry).

## Functions

<span class="name">add</span> (script_name, ..., vulnerabilities)  
Adds vulnerability tables into the vulnerability database (registry).

This function takes a variable number of vulnerability tables and stores them in the vulnerability database if they satisfy the callback filters that were registered by the `vulns.save_reports()` function.

Scripts must call `vulns.save_reports()` function first to setup the vulnerability database.

### Parameters

script_name  
The script name. The `SCRIPT_NAME` environment variable will do the job.

...  
 

vulnerabilities  
A variable number of vulnerability tables.

### Usage:

    local vuln_table = {
     title = "Vulnerability X",
     state = vulns.STATE.VULN,
     ...,
     -- take a look at the vulnerability table example at the beginning.
    }
    local status, ret = vulns.add(SCRIPT_NAME, vuln_table)

### Return values:

1.  True if the vulnerability tables were added, otherwise False.
2.  Number of added vulnerabilities on success.

<span class="name">add_ids</span> (fid, ..., FILTER, IDs)  
Add vulnerability IDs type to the vulnerability database associated with the `FILTER ID`.

This function will create a table for each specified vulnerability ID into the vulnerability database to store the associated vulnerability entries.

This function takes a `FILTER ID` as it is returned by the `vulns.save_reports()` function and a variable number of vulnerability IDs type as parameters.

Scripts must call `vulns.save_reports()` function first to setup the vulnerability database.

### Parameters

fid  
 

...  
 

FILTER  
ID as it is returned by `vulns.save_reports()`

IDs  
A variable number of strings that represent the vulnerability IDs type.

### Usage:

    vulns.add_ids(fid, 'CVE', 'OSVDB')

<span class="name">add_popular_id</span> (self, id_type, callback)  
Registers and associates a callback function with the popular ID vulnerability type to construct and return popular links automatically.

The callback function takes a vulnerability ID as a parameter and must return a link. The library automatically supports three different popular IDs: `CVE`: cve.mitre.org `OSVDB`: osvdb.org `BID`: www.securityfocus.com/bid

### Parameters

self  
 

id_type  
String representing the vulnerability ID type. `'CVE'`, `'OSVDB'` ...

callback  
A function to construct and return links.

### Usage:

    function get_example_link(id)
      return string.format("%s%s",
               "http://example.com/example?name=", id)
    end
    report:add_popular_id('EXM-ID', get_example_link)

### Return value:

True on success or false if it can not register the callback.

<span class="name">add_vulns</span> (self, ..., vulnerabilities)  
Adds vulnerability tables to the report.

Takes a variable number of vulnerability tables and stores them in the internal db of the report so they can be reported later.

### Parameters

self  
 

...  
 

vulnerabilities  
A variable number of vulnerability tables.

### Usage:

    local vuln_table = {
     title = "Vulnerability X",
     state = vulns.STATE.VULN,
     ...,
     -- take a look at the vulnerability table example at the beginning.
    }
    local status, ret = report:add_vulns(vuln_table)

### Return values:

1.  True if the vulnerability tables were added, otherwise False.
2.  Number of added vulnerabilities on success.

<span class="name">find</span> (fid, selection_filter, FILTER, selection)  
Search and return vulnerabilities in a list.

This function will return a list of the vulnerabilities that were stored in the vulnerability database associated with the `FILTER ID` that satisfy the `selection filter`. It will take a `FILTER ID` as it is returned by the `vulns.save_reports` function and a `selection_filter` table as parameters.

Scripts must call `vulns.save_reports()` function first to setup the vulnerability database.

This function is not affected by the `vulns.showall` script argument. The `selection_filter` is an optional table parameter of optional fields which can be used to select which vulnerabilities to return, if it is not set then all vulnerability entries will be returned.

### Parameters

fid  
 

selection_filter  
 

FILTER  
ID as it is returned by `vulns.save_reports()`

selection  
An optional table to select which vulnerabilities to list. The fields of the selection filter table are: state: The vulnerability state. risk_factor: The vulnerability `risk_factor` field, can be one of these values: `"High"`, `"Medium"` or `"Low"`. hosts_filter: A function to filter the `host` table of the vulnerability table. This function must return a boolean, true if it passes the filter otherwise false. The `host` table: host = {ip, targetname, bin_ip} ports_filter: A function to filter the `port` table of the vulnerability table. This function must return a boolean, true if it passes the filter, otherwise false. The `port` table: port = {number, protocol, service, version} id_type: The vulnerability ID type, (e.g: 'CVE', 'OSVDB' ...) id: The vulnerability ID. All these fields are optional.

### Usage:

    -- All the following fields are optional.
    local selection_filter = {
      state = vulns.STATE.VULN, -- number
      risk_factor = "High", -- string
      hosts_filter = function(vuln_table.host)
                     -- Function that returns a boolean
                     -- True if it passes the filter, otherwise false.
                     end,
                     -- vuln_table.host = {ip, targetname, bin_ip}
      ports_filter = function(vuln_table.port)
                     -- Function that returns a boolean
                     -- True if it passes the filter, otherwise false.
                     end,
                     -- vuln_table.port = {number, protocol, service
                     --                    version}
      id_type = 'CVE', -- Vulnerability type ID (string)
      id = 'CVE-XXXX-XXXX', -- CVE id (string)
    }
    local list = vulns.find(fid, selection_filter)

### Return value:

List of vulnerability tables on success, or nil on failures.

<span class="name">find_by_id</span> (fid, vuln_id_type, id, FILTER)  
Search vulnerability entries by ID and return the results in a list.

This function will return a list of the same vulnerability that affects different hosts, each host will have its own vulnerability table.

Scripts must call `vulns.save_reports()` function first to setup the vulnerability database.

### Parameters

fid  
 

vuln_id_type  
A string representing the vulnerability ID type.

id  
The vulnerability ID.

FILTER  
ID as it is returned by `vulns.save_reports()`

### Usage:

    local list = vulns.find_by_id(fid, 'CVE', 'CVE-XXXX-XXXX')

### Return value:

List of vulnerability tables on success, or nil on failures.

<span class="name">format_vuln</span> (vuln_table, showall)  
Format the vulnerability information and return it as a string.

This function can return nil if the vulnerability mandatory fields are missing or if the script argument `vulns.showall` and the `'showall'` string parameter were not set and the state of the vulnerability is `NOT VULNERABLE`.

Script writers must check the returned result.

If the vulnerability table contains the `host` and `port` tables, then the following fields will be shown: `vuln_table.host.targetname`, `vuln_table.host.ip`, `vuln_table.port.number` and `vuln_table.port.service`

### Parameters

vuln_table  
The vulnerability information table.

showall  
A string if set then show all the vulnerabilities including the `NOT VULNERABLE` ones. This optional parameter can be used to overwrite the `vulns.showall` script argument value.

### Usage:

    local vuln_str = vulns.format_vuln(vuln_table, 'showall')
    if vuln_str then
       return vuln_str
    end

### Return value:

Multiline string on success. If one of the mandatory vulnerability fields is missing or if the script argument `vulns.showall` and the `'showall'` string parameter were not specified and the vulnerability state is `NOT VULNERABLE` then it will print a debug message about the vulnerability and return nil.

<span class="name">format_vuln_table</span> (vuln_table, showall)  
Format the vulnerability information and return it in a table.

This function can return nil if the vulnerability mandatory fields are missing or if the script argument `vulns.showall` and the `'showall'` string parameter were not set and the state of the vulnerability is `NOT VULNERABLE`.

Script writers must check the returned result.

If the vulnerability table contains the `host` and `port` tables, then the following fields will be shown: `vuln_table.host.targetname`, `vuln_table.host.ip`, `vuln_table.port.number` and `vuln_table.port.service`

### Parameters

vuln_table  
The vulnerability information table.

showall  
A string if set then show all the vulnerabilities including the `NOT VULNERABLE` ones. This optional parameter can be used to overwrite the `vulns.showall` script argument value.

### Usage:

    local vuln_output = vulns.format_vuln_table(vuln_table)
    if vuln_output then
       -- process the vuln_output table
    end

### Return value:

Multiline string on success. If one of the mandatory vulnerability fields is missing or if the script argument `vulns.showall` and the `'showall'` string parameter were not specified and the vulnerability state is `NOT VULNERABLE` then it will print a debug message about the vulnerability and return nil.

<span class="name">get_ids</span> (fid, FILTER)  
Gets the vulnerability database associated with the `FILTER ID`.

This function can be used to check if there are vulnerability entries that were saved in the vulnerability database. The format of the vulnerability database associated with the `FILTER ID` is specified as Lua comments in this library.

Scripts must call `vulns.save_reports()` function first to setup the vulnerability database.

### Parameters

fid  
 

FILTER  
ID as it is returned by `vulns.save_reports()`

### Usage:

    local vulndb = vulns.get_ids(fid)
    if vulndb then
       -- process vulnerability entries
    end

### Return value:

vulndb The internal vulnerability database associated with the `FILTER ID` if there are vulnerability entries that were saved, otherwise nil.

<span class="name">get_popular_link</span> (id_type, id)  
Calls the function associated with the popular ID vulnerability type to construct and to return the appropriate reference link.

The library automatically supports three different popular IDs: `CVE`: cve.mitre.org `OSVDB`: osvdb.org `BID`: www.securityfocus.com/bid

### Parameters

id_type  
String representing the vulnerability ID type. `'CVE'`, `'OSVDB'` ...

id  
String representing the vulnerability ID.

### Usage:

    local link = vulns.get_popular_link('CVE', 'CVE-2001-0053')

### Return value:

URI The URI on success or nil if the library does not support the specified `id_type`, and in this case you can register new ID types by calling `vulns.register_popular_id()`.

<span class="name">lookup_id</span> (fid, vuln_id_type, id, FILTER)  
Lookup for a vulnerability entry in the vulnerability database associated with the `FILTER ID`.

This function can be used to see if there are any references to the specified vulnerability in the database, it will return `True` if so which means that one of the scripts has attempted to check this vulnerability.

Scripts must call `vulns.save_reports()` function first to setup the vulnerability database.

### Parameters

fid  
 

vuln_id_type  
A string representing the vulnerability ID type.

id  
The vulnerability ID.

FILTER  
ID as it is returned by `vulns.save_reports()`

### Usage:

    local status = vulns.lookup(fid, 'CVE', 'CVE-XXXX-XXXX')

### Return value:

True if there are references to this entry in the vulnerability database, otherwise False.

<span class="name">make_output</span> (self, ..., vulnerabilities)  
Report vulnerabilities.

Takes a variable number of vulnerability tables and stores them in the internal db of the report, then format all the vulnerabilities that are in this db for user display. Scripts should use this function as a tail call.

To show the `NOT VULNERABLE` entries users must specify the `vulns.showall` script argument.

### Parameters

self  
 

...  
 

vulnerabilities  
A variable number of vulnerability tables.

### Usage:

    local vuln_table = {
     title = "Vulnerability X",
     state = vulns.STATE.VULN,
     ...,
     -- take a look at the vulnerability table example at the beginning.
    }
    return report:make_output(vuln_table)

### Return value:

multiline string on success, or nil on failures.

<span class="name">make_output</span> (self, ..., vulnerabilities)  
Report vulnerabilities.

Takes a variable number of vulnerability tables and stores them in the internal db of the report, then format all the vulnerabilities that are in this db for user display. Scripts should use this function as a tail call.

To show the `NOT VULNERABLE` entries users must specify the `vulns.showall` script argument.

### Parameters

self  
 

...  
 

vulnerabilities  
A variable number of vulnerability tables.

### Usage:

    local vuln_table = {
     title = "Vulnerability X",
     state = vulns.STATE.VULN,
     ...,
     -- take a look at the vulnerability table example at the beginning.
    }
    return report:make_output(vuln_table)

### Return value:

multiline string on success, or nil on failures.

<span class="name">new</span> (self, script_name, host, port)  
Creates a new Report object

### Parameters

self  
 

script_name  
 

host  
 

port  
 

### Return value:

report object

<span class="name">register_popular_id</span> (id_type, callback)  
Registers and associates a callback function with the popular ID vulnerability type to construct and return popular links automatically.

The callback function takes a vulnerability ID as a parameter and must return a link. The library automatically supports three different popular IDs: `CVE`: cve.mitre.org `OSVDB`: osvdb.org `BID`: www.securityfocus.com/bid

### Parameters

id_type  
String representing the vulnerability ID type. `'CVE'`, `'OSVDB'` ...

callback  
A function to construct and return links.

### Usage:

    function get_example_link(id)
      return string.format("%s%s",
               "http://example.com/example?name=", id)
    end
    vulns.register_popular_id('EXM-ID', get_example_link)

### Return value:

True on success or false if it can not register the callback.

<span class="name">save_reports</span> (filter_callback)  
Initializes the vulnerability database and instructs the library to save all the vulnerability tables reported by scripts into this database (registry).

Usually this function should be called during a `prerule` function so it can instructs the library to save vulnerability entries that will be reported by the `vulns.Report` class or by the `vulns.add()` function.

This function can take an optional callback filter parameter that can help the library to decide if it should store the vulnerability table in the registry or not. The callback function must return a boolean value. If this parameter is not set then all vulnerability tables will be saved. This function will return a uniq `FILTER ID` for the scripts to be used by the other library functions to reference the appropriate vulnerability entries that were saved previously.

### Parameters

filter_callback  
The callback function to filter vulnerabilities. The function will receive a vulnerability table as a parameter in order to inspect it, and must return a boolean value. True if the the vulnerability table should be saved in the registry, otherwise false. This parameter is optional.

### Usage:

    FID = vulns.save_reports() -- save all vulnerability reports.

    -- Save only vulnerabilities with the <code>VULNERABLE</code> state.
    local function save_only_vuln(vuln_table)
      if (vuln_table.state & vulns.STATE.VULN) ~= 0 then
        return true
      end
      return false
    end
    FID = vulns.save_reports(save_only_vuln)

### Return value:

Filter ID A uniq ID to be used by the other library functions to reference and identify the appropriate vulnerabilities.

</div>

</div>

</div>

<img src="/shared/images/nst-icons.svg#search" style="width:100%;aspect-ratio:1/1;" aria-hidden="true" />

<div class="flexlists">

<div class="fl-unit">

## <a href="https://nmap.org/" class="nlink">Nmap Security Scanner</a>

- <a href="https://nmap.org/book/man.html" class="nlink">Ref Guide</a>
- <a href="https://nmap.org/book/install.html" class="nlink">Install Guide</a>
- <a href="https://nmap.org/docs.html" class="nlink">Docs</a>
- <a href="https://nmap.org/download.html" class="nlink">Download</a>
- <a href="https://nmap.org/oem/" class="nlink">Nmap OEM</a>

</div>

<div class="fl-unit">

## <a href="https://npcap.com/" class="nlink">Npcap packet capture</a>

- <a href="https://npcap.com/guide/" class="nlink">User's Guide</a>
- <a href="https://npcap.com/guide/npcap-devguide.html#npcap-api" class="nlink">API docs</a>
- <a href="https://npcap.com/#download" class="nlink">Download</a>
- <a href="https://npcap.com/oem/" class="nlink">Npcap OEM</a>

</div>

<div class="fl-unit">

## <a href="https://seclists.org/" class="nlink">Security Lists</a>

- <a href="https://seclists.org/nmap-announce/" class="nlink">Nmap Announce</a>
- <a href="https://seclists.org/nmap-dev/" class="nlink">Nmap Dev</a>
- <a href="https://seclists.org/fulldisclosure/" class="nlink">Full Disclosure</a>
- <a href="https://seclists.org/oss-sec/" class="nlink">Open Source Security</a>
- <a href="https://seclists.org/dataloss/" class="nlink">BreachExchange</a>

</div>

<div class="fl-unit">

## <a href="https://sectools.org" class="nlink">Security Tools</a>

- <a href="https://sectools.org/tag/vuln-scanners/" class="nlink">Vuln scanners</a>
- <a href="https://sectools.org/tag/pass-audit/" class="nlink">Password audit</a>
- <a href="https://sectools.org/tag/web-scanners/" class="nlink">Web scanners</a>
- <a href="https://sectools.org/tag/wireless/" class="nlink">Wireless</a>
- <a href="https://sectools.org/tag/sploits/" class="nlink">Exploitation</a>

</div>

<div class="fl-unit">

## <a href="https://insecure.org/" class="nlink">About</a>

- <a href="https://insecure.org/fyodor/" class="nlink">About/Contact</a>
- <a href="https://insecure.org/privacy.html" class="nlink">Privacy</a>
- <a href="https://insecure.org/advertising.html" class="nlink">Advertising</a>
- <a href="https://nmap.org/npsl/" class="nlink">Nmap Public Source License</a>

</div>

<div class="fl-unit social-links">

<a href="https://twitter.com/nmap" class="nlink" title="Visit us on Twitter"><img src="/shared/images/nst-icons.svg#twitter" aria-hidden="true" width="32" height="32" /></a> <a href="https://facebook.com/nmap" class="nlink" title="Visit us on Facebook"><img src="/shared/images/nst-icons.svg#facebook" aria-hidden="true" width="32" height="32" /></a> <a href="https://github.com/nmap/" class="nlink" title="Visit us on Github"><img src="/shared/images/nst-icons.svg#github" aria-hidden="true" width="32" height="32" /></a> <a href="https://reddit.com/r/nmap/" class="nlink" title="Discuss Nmap on Reddit"><img src="/shared/images/nst-icons.svg#reddit" aria-hidden="true" width="32" height="32" /></a>

</div>

</div>

</div>