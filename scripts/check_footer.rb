# frozen_string_literal: true

# Exercise the actual footer with the Liquid version used by GitHub Pages.
require "liquid"
require "cgi"

module FooterFilters
  def escape(value)
    CGI.escapeHTML(value.to_s)
  end

  def relative_url(value)
    "/docs/#{value}"
  end
end

Liquid::Template.register_filter(FooterFilters)
source = File.read(File.expand_path("../_includes/footer.html", __dir__))
source = source.sub("{% include footer_custom.html %}", "")
template = Liquid::Template.parse(source, error_mode: :strict)
repo = "https://github.com/UnitVectorY-Labs/example"
cases = {
  "unset" => {},
  "empty" => { "license" => "" },
  "false" => { "license" => false },
  "URL only" => { "license_url" => "https://example.com/license" },
  "MIT" => { "license" => "MIT License", "license_url" => "#{repo}/blob/main/LICENSE" },
  "Apache" => { "license" => "Apache-2.0 License", "license_url" => "#{repo}/blob/main/LICENSE" },
  "custom" => { "license" => "Terms & conditions", "license_url" => "https://example.com/terms?a=1&b=2" },
  "fallback URL" => { "license" => "MIT License" }
}

cases.each do |name, settings|
  site = { "uvy_docs" => settings, "gh_edit_repository" => repo, "gh_edit_branch" => "release" }
  html = template.render!({ "site" => site }, strict_filters: true)
  links = html.scan(/<a href="([^"]*)">(.*?)<\/a>/m)
  enabled = settings["license"] && settings["license"] != ""
  expected_links = enabled ? 3 : 2
  raise "#{name}: unexpected links #{links.inspect}" unless links.length == expected_links
  raise "#{name}: unexpected separators" unless html.scan('class="footer-sep"').length == expected_links - 1
  raise "#{name}: missing repository" unless links.last.first == repo
  next unless enabled

  url = settings["license_url"] || "#{repo}/blob/release/LICENSE"
  raise "#{name}: incorrect license" unless links[1] == [CGI.escapeHTML(url), CGI.escapeHTML(settings["license"])]
end

puts "Passed #{cases.length} footer license cases"
