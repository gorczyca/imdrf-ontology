# IMDRF

This contains ontologies based on the _International Medical Device Regulators Forum_ (IMDRF) terms for Categorized Adverse Events Reporting: https://www.imdrf.org/documents/terminologies-categorized-adverse-event-reporting-aer-terms-terminology-and-codes 

The [files](./sources) consist of the following annexes:

- [Annex A](./sources/annexa_3.json): Medical Device Problem
- [Annex B](./sources/annexb_1.json): Type of Investigation
- [Annex C](./sources/annexc_1.json):  Investigation Findings
- [Annex D](./sources/annexd_1.json):  Investigation Conclusion
- [Annex E](./sources/annexe_1.json):  Health Effects - Clinical Signs and Symptoms or Conditions
- [Annex F](./sources/annexf_1.json):  Health Effects - Health Impact
- [Annex G](./sources/annexg_1.json): Medical Device Component

The terms are structured in hierarchies:

```
Term
└── Sub term 
    └── Sub-sub term
```

E.g. 
```
A17 - Compatibility Problem
└── A1701 - Component or Accessory Incompatibility
    └── A170101 - Accessory Incompatible
```