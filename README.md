## PyData Hacknight

### What is this?

PyData Cardiff organised a hacknight at Hodge House, Cardiff on the 13th of November 2025. This is the code to help set you up and hopefully show off some of the things that were built on the night. The data here is taken from [Tidy Tuesdays 2025-02-04 on the Simpsons](https://github.com/rfordatascience/tidytuesday/blob/main/data/2025/2025-02-04/simpsons_episodes.csv).

#### Disclaimer

Because this is scraped data that is nearly a decade old (see the references in the Tidy Tuesday repo and in kaggle), many (all?) of the URLS seem dead/broken.

### How do I get started?

(step 0 is to make sure you have a github account and install[git](https://github.com/git-guides) on your machine)

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repository
1. [Clone](https://github.com/git-guides/git-clone#git-clone) your forked repository to your local machine
1. Avoid modifying the `tidy_tuesdays_original` folder directly.
1. Make a folder with your github user name in the pydata_cardiff folder
    * You could even pair up with someone else and make a folder with both your user names
1. Write some code in the folder you created
    * The `pyproject.toml` can help bootstrap a [poetry](https://python-poetry.org/docs/) or [uv](https://docs.astral.sh/uv/) environment. Both of these can be installed with [pipx](https://pipx.pypa.io/stable/)
1. [Add](https://github.com/git-guides/git-add) your code the folder

### What do I make?

1. Anything you want! If you think you might be able to do it, have a go. Think about what you want to learn, and try to do that. Or maybe think about what you believe to be true about the Simpsons and see if you can prove it from the data.

(But if you are stuck for ideas heres a few)

### Topic Specific Ideas

* Does the Simpsons pass the [Bechdel Test](https://en.wikipedia.org/wiki/Bechdel_test)
* Analyse which member of the Simposons family is the most important by creating a ['network of characters'](https://web.madstudio.northwestern.edu/re-visualizing-the-novel/) diagram.
* Visualise each characters lines as a word cloud

### Tool Specific Ideas

* Create an [interactive dashboard](https://plotly.com/python/) slice and dice the data
* Graph data in a [backend agnostic](https://narwhals-dev.github.io/narwhals/why/) way
    * `daveparr/joinar` joins the datasets in this project in a backend agnostic way. 
        * If you're keen to collab on this (tests, new features, even just docs!) come grab me :)
* Create an [backend server to return specific data](https://fastapi.tiangolo.com/)
* Create a [cli to return specific data](https://typer.tiangolo.com/)
* Create data schemas for [data validation](https://pandera.readthedocs.io/en/stable/index.html#)

### Data Specific Ideas

> Use scraping tools responsibly, and where present respect [robots.txt](https://en.wikipedia.org/wiki/Robots.txt) and comply with [Really Simple Licensing](https://rslstandard.org/)

* Can the urls in the data set be updated/ replaced?
* Can the data set be updated with current episodes?
* Can the data set be extended with other data sources? 
    * [Simpsons Wiki](https://simpsons.fandom.com/wiki/Simpsons_Wiki) for instance...

### Machine Learning Specific Ideas

* Predict the rating of a given episode based on the presence of specific characters
* Classify episodes into specific ['topics'](https://www.datacamp.com/tutorial/what-is-topic-modeling)

### AI Specific Ideas

* A summary index of the key plot points of each episode
* AI images of specific scenes by prompting using the script data
* A couch gag generator that outlines a new couch gag based on the themes each episode

### Alternative Data Science Language Hipster Challenge

* Pick a simple problem you can confidently do in Python such as a simple plot of variables or a linear regression model, then try to re-create an equivalent in another 'data science' language, such as `R`, `Julia` or `Mojo`. A few languages that [might not seem like data science languages](https://github.com/pola-rs/nodejs-polars) also [might surprise you](https://rust-ml.github.io/book/5_linear_regression.html).

> @DaveParr does not take any responsibility for the quality of the ideas listed above. For any given idea it may be too hard, too easy, or just plain stupid.

Other folks have worked with this data before:

[kaggle](https://www.kaggle.com/datasets/prashant111/the-simpsons-dataset/code)


### What if I have questions?

1. Ask someone near you, they're probably really nice.
1. Google it, reading the docs isn't cheating!
1. Ask one of the organisers.

### What do I do when I am done?

1. [Commit](https://github.com/git-guides/git-commit#git-commit) your changes to your local repository.
1. [Push](https://github.com/git-guides/git-push) your changes to your forked repository.
1. Create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) to merge your changes into this repository.
1. Tag @DaveParr for review
1. Use your new knowledge to forage for donuts and Duff Beer