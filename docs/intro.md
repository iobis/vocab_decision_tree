This decision tree is a tool to assist with finding and selecting appropriate controlled vocabulary to be used in the extended Measurement or Fact (eMoF) extension of Darwin Core. For those unfamiliar with the tree see the [OBIS YouTube Vocabulary series](https://www.youtube.com/playlist?list=PLlgUwSvpCFS4hADB7Slf44V1KJauEU6Ul) and the [relevant section of the OBIS manual](https://manual.obis.org/vocabulary.html#controlled-vocabulary-for-emof).

# How to Use

When populating a table for the eMoF extension, you should use controlled vocabularies for fields like `measurementType`, `measurementValue`, and `measurementUnit`. Importantly, the corresponding identifier terms—`measurementTypeID`, `measurementValueID`, and `measurementUnitID`—should be used to reference standardized, machine-readable URIs that ensure clarity and consistency across datasets. OBIS recommends vocabularies from the [NERC Vocabulary Server](http://www.bodc.ac.uk/resources/products/web_services/vocab/), though any URI-based controlled vocabulary may be used. 

Click on the nodes of this tree to help you walk through the logic of picking appropriate terms from OBIS recommended vocabularies.


# Credits

This tool was built by the OBIS Vocabulary Team, led by Elizabeth Lawrence. It is based on the Interactive Flowchart template developed within [Urban Complexity Lab (UCLAB)](https://uclab.fh-potsdam.de/) at University of Applied Sciences Potsdam and is licensed under an [MIT license](https://github.com/uclab-potsdam/interactive-flowchart/blob/main/LICENSE).