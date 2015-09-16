`Anatolik` is a tool that helps you to build your own static site.

It's build for me by me and I don't think it will fits your needs. As a person
with heavy NIH syndrom I was not satisfied with existing static blogging
systems, so I made my own. Yay!

My needs:

* Python. I need a system that I can talk to in it's native language.
* Python 3. Yes, exactly third version, because I speak russian and need
  unicode support. Also I don't want system that developed for outdated version
  of language.
* Content interlinks. I need to reference to other of my post.
* Simplicity. No social bullshit, no comments, just as little as possible.

None of existing static blogging platforms have fit me, so here where I am and
that's why I'm releasing this.

Dependencies
------------

* python3
* pyatom
* PyYAML
* pypandoc
* mako
* requests

How it works
------------

Anatolik operates on Site with Posts, Layouts and Pages.

- Site is a global object that contains general information about whole site.
- Posts are content documents. Posts must supply layout to use. Posts are
translated into HTML. Posts can have templates.
- Layouts are markup documents that wraps translated posts. Layouts can also have
templates.
- Pages are final stage. Page it's a processed layout with content.

	+------------------------+
	|                        |
	|         Page           |
	|                        |
	|      (Pure HTML)       |
	|                        |
	+------------------------+
				^
				|
				|
	   Templates processing
				|
		 Content insertion
				|
				|
	+------------------------+
	|                        |
	|        Layout          |
	|                        |
	|   (HTML + Templates)   |
	|                        |
	+------------------------+
				^
				|
				|
	   Templats processing
				|
	   Translation to HTML
				|
				|
	+------------------------+
	|                        |
	|        Content         |
	|                        |
	| (Markdown + Templates) |
	|                        |
	+------------------------+

From the top view compilation process is following

0. Build site map.
   Site map is hash map accessible from every component that contains:
   * Configuration;
   * Paths to posts, layouts, output, assets;
   * Lists of content posts, layouts objects (filled during processing).

   Mainly this map is used in templates such as %{ site.url } or 
   %{ site.posts['some-post'] }.

1. Process layouts.
   For every layout:
   * Parse layout file and instantiate Layout object;
   * Render layout templates.

2. Process posts.
   For every content post:
   * Parse post file and instantiate Post object;
   * Render post templates;
   * Convert to HTML.

3. For every post.
   * Instantiate Page object from post and corresponding layout;
   * Insert post in layout;
   * Store Page in output directory under given directory.

4. Put assets in output.


Templating
----------

Templating is done with Mako templates.

Each post are given 2 dictionaries:

1. `site` - global configuration object. site members:
    * `posts` - list of all posts
    * `layouts` - list of all layouts
    * `url` - site URL
1. `post` - current post object

<!-- vim: set ft=markdown: -->
