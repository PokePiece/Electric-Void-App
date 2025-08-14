{
  "targets": [
    {
      "target_name": "math",
      "sources": [ "native/math.cpp" ],
      "include_dirs": [
        "<!(node -e \"require('nan')\")"
      ]
    }
  ]
}