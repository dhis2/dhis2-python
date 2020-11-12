# dhis2-python: integration client for dhis2

[![Package version](https://badge.fury.io/py/dhis2.svg)](https://pypi.python.org/pypi/dhis2)

**Requirements**: Python 3.8+

## Quickstart

Install using `pip`:

```shell
$ pip install dhis2
```

This will install the `dhis2` command in your local environment (installing into a virtual environment recommended).

The tool supports a pluggable architecture, but the core supports:

* Inspecting dhis2 instances
    * `dhis2 -i inventory.yml inspect host-id/group-id`
* Extracting mCSD and SVCM compatible payload, and pushing those to a FHIR compliant server
    * `dhis2 -i inventory.yml facility-list mcsd mcsd-config.yml`
    * `dhis2 -i inventory.yml code-list svcm svcm-config.yml`
* Extract ICD 11 (MMS) `LinearizationEntities` as DHIS2 Option Sets
  * `dhis2 -i inventory.yml code-list icd11 <icd11-host> --root-id <X>`
* Extract ICD 10 `ICD10Entities` as DHIS2 Option Sets
  * `dhis2 -i inventory.yml code-list icd10 <icd10-host> --root-id <X>`
  * Please be aware that the icd11 docker image does _not_ include the icd10 code lists, so you have to use the public instance which requires API keys

(see description of formats below)

As of now, we do not support sending data to dhis2, only extraction is supported.

## Formats

### Inventory

The inventory is where you will store all your services, and various groupings you might find useful (most commands will only work on single sources/targets though, with the exception of the `inspect` command currently)

The basic format is as follows

```yaml
hosts:
  playdev:
    type: dhis2
    baseUrl: https://play.dhis2.org/dev
    username: admin
    password: district
  playdemo:
    type: dhis2
    baseUrl: https://play.dhis2.org/demo
    auth:
      default:
        type: http-basic
        username: admin
        password: district
  fhirdemo:
    type: fhir
    baseUrl: http://localhost:8080
  icd11local:
    type: icd11
    baseUrl: http://localhost:8888
  icd11official:
    type: icd11
    baseUrl: https://id.who.int
    headers:
      Authorization: Bearer YOUR_TOKEN
  icd10official:
    type: icd10
    baseUrl: https://id.who.int
    headers:
      Authorization: Bearer YOUR_TOKEN
groups:
  dhis2:
    - playdev
    - playdemo
```

The keys of the `hosts` and `groups` block will be used to identifiy targets when using the `dhis2` commands.

Please note that:

* Currently only `http-basic` is supported for dhis2
* For fhir no authentication is supported (coming soon)

### mCSD / SVCM configuration

Both mCSD and SVCM currently has the exact same format so we will describe them together. You will need a source host, target host (or some other target) and a set of filters if desired.

Basic format

```yaml
source:
  id: playdev
target:
  id: fhirdemo
```

This configuration would simply take all org unit or option sets inside of dhis2 and push them to a fhir instance.

If you would want to store the result instead, you can use the `log://` target

```yaml
source:
  id: playdev
target:
  id: log://

```

(this is also the default if no target is given)
