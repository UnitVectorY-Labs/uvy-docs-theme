# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "uvy-docs-theme"
  spec.version       = "0.2.0"
  spec.authors       = ["UnitVectorY-Labs"]
  spec.summary       = "UnitVectorY-Labs documentation theme for Jekyll and GitHub Pages."
  spec.homepage      = "https://github.com/UnitVectorY-Labs/uvy-docs-theme"
  spec.license       = "MIT"

  spec.files         = Dir.glob("{_layouts,_includes,_sass,assets}/**/*") + ["LICENSE", "README.md"]

  spec.add_runtime_dependency "jekyll", ">= 3.9", "< 5.0"
end
