# H5Media
Media player app written using HTML5


## Coding Standards

### HTML

* Use camelcase for id values (i.e. `id="addToPlaylistDialog"`)
* Use hyphens for css classes (i.e. `class="podcast-descriptions"`)

### URLS (& Django urlconf)

* If needed, place hyphens in url (i.e. `password-reset`)
* Template names should match the name of the view.  (i.e. if the name of the 
view is `'podcasts'` than the template should be `'podcasts.html'`
* The url names should match the view names.  (i.e. if the view is 
`PodcastEpisodeListView` than the view should be named `'podcast_episode_list'`) 

### Python/Django

* View classes should have a name ending in "View"

