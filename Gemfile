source "https://rubygems.org"

gem "jekyll", "~> 4.4"
gem "minimal-mistakes-jekyll", "~> 4.27"

# Plugins. jekyll-include-cache is required by Minimal Mistakes.
group :jekyll_plugins do
  gem "jekyll-include-cache"
  gem "jekyll-feed"
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
end

# Ruby 3.4 removed these from the standard library.
gem "csv"
gem "base64"
gem "bigdecimal"
gem "logger"

# Faster file watching on macOS during `bundle exec jekyll serve`.
gem "wdm", "~> 0.1", platforms: [:mingw, :x64_mingw, :mswin]
