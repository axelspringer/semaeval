About
=====

Semaeval is a python package to evaluate the quality of semantic engines. We support evaluation of the following engines:

- [www.alchemyapi.com](http://www.alchemyapi.com)
- [www.basistech.com](http://www.basistech.com)
- [www.bitext.com](http://www.bitext.com)
- [nlp.linguasys.com](http://nlp.linguasys.com)
- [www.meaningcloud.com](http://www.meaningcloud.com)
- [www.netowl.com](http://www.netowl.com)
- [www.repustate.com](http://www.repustate.com)
- [www.retresco.de](http://www.retresco.de)
- [www.semantria.com](http://semantria.com)
- [www.temis.com](http://www.temis.com)
- [www.textrazor.com](http://www.textrazor.com/)

Semaeval also offers tools to get example texts from the following sources:

- [www.bild.de](http://www.bild.de)
- [www.welt.de](http://www.welt.de)
- [www.axelspringer-syndication.de](http://www.axelspringer-syndication.de/)
- [www.fakt.pl](http://www.fakt.pl/)
- [www.huffingtonpost.fr](http://www.huffingtonpost.fr/)

Installation
------------

Make sure you have Python 2.7 with pip and setuptools installed. Then clone the git repository and execute
the following commands in the repository folder:

    pip install numpy matplotlib
    python setup.py install

This will install numpy and the semaeval package and all the necessary dependencies into your python environment.

To use the package you have to create a file `config.yml` holding the configuration for all the semantic engines
you want to use. To do this copy the template file `config_template.yml` and edit it with an editor of your choice:

    cp config_template.yml config.yml
    nano config.yml

In the config file you will find configuration options for all the supported engines:

    folder_input: "input"
    folder_output: "output"
    # categories can be one of these:
    # PERSON, GEO, ORG, PRODUCT, EVENT, KEYWORD, FUNCTION, NUMBER, DATE, CURRENCY, URL, QUOTE
    categories:
      - PERSON
      - GEO
      - ORG
    engines:
      simple:
        labels:
          "GPE": "GEO"
          "LOCATION": "GEO"
          "ORGANIZATION": "ORG"
          "PERSON": "PERSON"
          "FACILITY": "KEYWORD"
          "GSP": "ORG"
    #  alchemy:
    #    key:
    #    # see http://www.alchemyapi.com/api/entity/types
    #    labels:
    #      "City": "GEO"
    #      "Facility": "GEO"
    #      "StateOrCounty": "GEO"
    #      "Country": "GEO"
    #      "Region": "GEO"
    #      "Continent": "GEO"
    #      "GeographicFeature": "GEO"
    #      "Person": "PERSON"
    #      "Company": "ORG"
    #      "Organization": "ORG"
    #      "PrintMedia": "ORG"
    #      "JobTitle": "FUNCTION"
    #      "Quantity": "NUMBER"
    #      "SportingEvent": "EVENT"
    #      "Drug": "KEYWORD"
    #      "HealthCondition": "KEYWORD"
    #      "FieldTerminology": "KEYWORD"
    #      "Sport": "KEYWORD"
    #      "Technology": "KEYWORD"
    #      "EntertainmentAward": "KEYWORD"
    #      "Holiday": "EVENT"
    #      "TelevisionStation": "ORG"
    #      "Crime": "KEYWORD"

To activate e.g. alchemy uncomment the alchemy section in the configuration file and enter your alchemy key like

    folder_input: "input"
    folder_output: "output"
    # categories can be one of these:
    # PERSON, GEO, ORG, PRODUCT, EVENT, KEYWORD, FUNCTION, NUMBER, DATE, CURRENCY, URL, QUOTE
    categories:
      - PERSON
      - GEO
      - ORG
    engines:
      simple:
        labels:
          "GPE": "GEO"
          "LOCATION": "GEO"
          "ORGANIZATION": "ORG"
          "PERSON": "PERSON"
          "FACILITY": "KEYWORD"
          "GSP": "ORG"
      alchemy:
        key: 1234567890
        # see http://www.alchemyapi.com/api/entity/types
        labels:
          "City": "GEO"
          "Facility": "GEO"
          "StateOrCounty": "GEO"
          "Country": "GEO"
          "Region": "GEO"
          "Continent": "GEO"
          "GeographicFeature": "GEO"
          "Person": "PERSON"
          "Company": "ORG"
          "Organization": "ORG"
          "PrintMedia": "ORG"
          "JobTitle": "FUNCTION"
          "Quantity": "NUMBER"
          "SportingEvent": "EVENT"
          "Drug": "KEYWORD"
          "HealthCondition": "KEYWORD"
          "FieldTerminology": "KEYWORD"
          "Sport": "KEYWORD"
          "Technology": "KEYWORD"
          "EntertainmentAward": "KEYWORD"
          "Holiday": "EVENT"
          "TelevisionStation": "ORG"
          "Crime": "KEYWORD"

If the content of your configuration file is like above, you have activated two engines for evaluation:
simple (which simply uses Python NLTK, this engines serves mainly as a baseline comparison) and
alchemy. For both engines label conversion is also configured. This is necessary to allow comparison of
the different results of each engine.

Getting started
---------------

You can use the semaeval package as follows:

    >>> import semaeval.source.welt as welt
    >>> import semaeval.evaluate as eval
    >>> import semaeval.statistics as stats
    >>> articles = welt.articles_from_feed()     # get the latest 20 articles from Welt RSS feed
    Wed, 08 Apr 2015 16:59:23 +0200
    http://www.welt.de/article139215840.html
    Wed, 08 Apr 2015 14:34:17 +0200
    http://www.welt.de/article139250110.html
    ...
    >>> articles_enriched = eval.detect_entities(articles,"de")  # this takes quite a while (depending on the number of configured engines and the number of articles)
    URL: http://www.welt.de/article139215840.html
    Collecting results:
    semaeval.engine.bitext.bitext
    semaeval.engine.meaningcloud.meaningcloud
    semaeval.engine.simple.simple
    semaeval.engine.linguasys.linguasys
    semaeval.engine.basistech.basistech
    semaeval.engine.semant.semant
    semaeval.engine.alchemy.alchemy
    semaeval.engine.txtrazor.txtrazor
    semaeval.engine.retresco.retresco
    ...
    >>> data = stats.collect_data(articles_enriched)    # Compute precision and recall for each category for each article and each engine
    >>> results = stats.aggregate_result(data)          # computing mean values for each category (PERSON, GEO, ORG, ...)
    >>> results.extend(stats.compute_total(results))    # compute an overall total average over all categories and add this TOTAL to the results
    >>> stats.plot_results(results)                     # show a plot of the results

Contact
-------

[Andreas Maier](https://github.com/asmaier) (andreas.maier@asideas.de).




