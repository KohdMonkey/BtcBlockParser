# BtcBlockParser

Parsing Bitcoin block header data

## getting the latest chain data
Simplified Payment Verification (SPV) nodes are sufficient for getting the
latest data since it only retrieves block headers, which is what we want. 

[Electrum](https://electrum.org/#download) is a popular Bitcoin client that
can serve as an SPV client. 

1. wget https://download.electrum.org/4.1.2/Electrum-4.1.2.tar.gz
2. tar -zxf Electrum-4.1.2.tar.gz
3. ./run\_electrum

Note: the latest version of electrum uses checkpoints and does not download 
the entire history of block headers. To retrieve the entire history, first
locate the file "checkpoints.json" inside the electrum subdirectory, and
remove all of the checkpoints inside. Once done, run the Electrum client.

The block headers are stored in a file called "blockchain\_headers". On Linux,
this file can be located at ~/.electrum. For other systems, consult the
[documentation](https://electrum.readthedocs.io/en/latest/faq.html#where-is-the-electrum-datadir-located)

## Block Headers
The block headers are stored sequentially as raw bytes. Each header is 80 bytes
long and consists of the fields
1. version number. 4 bytes
2. previous block hash. 32 bytes.
3. merkle root hash. 32 bytes
4. block time. 4 bytes
5. block difficulty. 4 bytes
6. block nonce. 4 bytes

For more information on each field, consult the [reference](https://developer.bitcoin.org/reference/block_chain.html)
