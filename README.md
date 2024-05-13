# Floor plan furniture parser

This challenge asks to parse a floor plan and extract the furniture from it. By provide a floor plan in a text file (see example.txt), the program should be able to extract the following information:

- Number of different chair types for the apartment
- Number of different chair types per room

## Usage

Clone the repository:

```bash
git clone git@github.com:Yagomfh/furniture-parser.git
```

Run the CLI using the following command:

```bash
python furniture_parser.py
```

## Example

Provide the path to the file containing the floor plan:

```bash
python furniture_parser.py
Path to your file (i.e. path/to/file): example.txt
```

Sample output:

```bash
total:
W: 14 P: 7 C: 1 S: 3
balcony:
W: 0 P: 2 C: 0 S: 0
bathroom:
W: 0 P: 1 C: 0 S: 0
closet:
W: 0 P: 3 C: 0 S: 0
kitchen:
W: 4 P: 0 C: 0 S: 0
living room:
W: 7 P: 0 C: 0 S: 2
office:
W: 2 P: 1 C: 0 S: 0
sleeping room:
W: 1 P: 0 C: 0 S: 1
toilet:
W: 0 P: 0 C: 1 S: 0
```
