import time

import petl as etl
import IPython
import pandas as pd

_DEBUG = True
_TIME_TEST = True

# Test case on run time complement vs antijoin.
# normally these would be toggles but for testing we set both to true
_COMPLEMENT = True
_ANTI_JOIN = True

# csv = comma delimited, tsv = tab delimited
pre_etl_time = time.time()
a = etl.fromtsv('snpdata.csv')
post_etl_time = time.time()
b = etl.fromtsv('popdata.csv')

pre_df_time = time.time()
df_a = pd.read_csv('snpdata.csv', sep='\t', header=0)
post_df_time = time.time()

print("ETL time to load A file: {} Pandas time to load A file: {}".format
      (post_etl_time-pre_etl_time, post_df_time-pre_df_time))

df_b = pd.read_csv('popdata.csv', sep='\t', header=0)

header_a = etl.header(a)
header_b = etl.header(b)
if _DEBUG:
    print(header_a)
    print(header_b)


b_renamed = b.rename({'Chromosome': 'Chr',
                      'Coordinates': 'Pos',
                      'Ref. Allele': 'Ref',
                      'Non-Ref. Allele': 'Nref',
                      'Derived Allele': 'Der',
                      'Mutation type': 'Mut',
                      'Gene': 'GeneId',
                      'Gene Aliases': 'GeneAlias',
                      'Gene Description': 'GeneDescr'})

df_b_renamed = df_b.rename(index=str, columns={'Chromosome': 'Chr',
                      'Coordinates': 'Pos',
                      'Ref. Allele': 'Ref',
                      'Non-Ref. Allele': 'Nref',
                      'Derived Allele': 'Der',
                      'Mutation type': 'Mut',
                      'Gene': 'GeneId',
                      'Gene Aliases': 'GeneAlias',
                      'Gene Description': 'GeneDescr'})
if _DEBUG:
    print("B renamed header: {}".format(b_renamed.header()))
    print("df B renamed header: {}".format(df_b_renamed.columns.values))

assert all(b_renamed.header() == df_b_renamed.columns.values), \
    "Df and ETL created different headers"

common_fields = ['Chr', 'Pos', 'Ref', 'Nref', 'Der', 'Mut', 'GeneId', 'GeneAlias', 'GeneDescr']
a_common = a.cut(common_fields)
b_common = b_renamed.cut(common_fields)

if _DEBUG:
    print(a_common)
    print(b_common)

    a_common.valuecounts('Mut')
    b_common.valuecounts('Mut')

a_conv = a_common.convert('Pos', int)
b_conv = (
    b_common
    .convert('Pos', int)
    .convert('Mut', {'SYN': 'S', 'NON': 'N'})
)

# highlight = 'background-color: yellow'
# magic command for pretty displaying data
# a_conv.display(caption='a', vrepr=repr, td_styles={'Pos': highlight})
# b_conv.display(caption='b', vrepr=repr, td_styles={'Pos': highlight, 'Mut': highlight})

# look for missing data
a_len = a_conv.nrows()
b_len = b_conv.nrows()

print("A length = {}, B length = {}".format(a_len, b_len))

# There are discrepancies between A/B tables,
# start by analyzing Chr and Pos columns

a_locs = a_conv.cut('Chr', 'Pos')
b_locs = b_conv.cut('Chr', 'Pos')

a_only_complement_list = []
a_only_antijoin_list = []

# antijoin for this dataset seems to tke 15-33% longer
if _TIME_TEST:
    if _COMPLEMENT:
        pre_complement_time = time.time()
        locs_only_in_a = a_locs.complement(b_locs)
        for a in range(0, 1000):
            a_only_complement_list.append([a_locs.complement(b_locs)])
        post_complement_time = time.time()
        print("Complement runs took: {} seconds".format
              (post_complement_time - pre_complement_time))
    if _ANTI_JOIN:
        pre_antijoin_time = time.time()
        locs_only_in_a = a_conv.antijoin(b_conv, key=('Chr', 'Pos'))
        for a in range(0, 1000):
            a_only_antijoin_list.append(
                a_conv.antijoin(b_conv, key=('Chr', 'Pos')))
        post_antijoin_time = time.time()
        print("Antijoin runs took: {} seconds".format
              (post_antijoin_time - pre_antijoin_time))

if _COMPLEMENT:
    locs_only_in_a = a_locs.complement(b_locs)
else:
    locs_only_in_a = a_conv.antijoin(b_conv, key=('Chr', 'Pos'))


a_only = locs_only_in_a.nrows()

print("A only rows (Chr and Pos columns): {}".format(a_only))

# magic command for IPython display
# locs_only_in_a.displayall(caption='a only')

locs_only_in_b = b_locs.complement(a_locs)
b_only = locs_only_in_b.nrows()

print("B only rows: {}".format(b_only))

# Export missing locations to csv
if a_only > 0:
    locs_only_in_a.tocsv('missing_locations_a.csv')
else:
    locs_only_in_b.tocsv('missing_locations_b.csv')

# find conflicts between A/B on Chr and Pos columns
ab_merge = etl.merge(a_conv, b_conv, key=('Chr', 'Pos'))
# magic command for IPython display
# ab_merge.display(caption='ab_merge',
#                  td_styles=lambda v: highlight if isinstance(v, etl.Conflict) else '')

# Create a new list of all conflicting values
ab = etl.cat(a_conv.addfield('source', 'a', index=0),
             b_conv.addfield('source', 'b', index=0))
ab_conflicts = ab.conflicts(key=('Chr', 'Pos'), exclude='source')

# magic command for IPython display
# ab_conflicts.display(10)

# Highlight specific conflicts
ab_conflicts_mut = ab.conflicts(key=('Chr', 'Pos'), include='Mut')

# magic command for IPython display
# ab_conflicts_mut.display(10, caption='Mut conflicts',
# td_styles={'Mut': highlight})
ab_conflict_num = ab_conflicts_mut.nrows()

if _DEBUG:
    print("Total number of A/B conflicts: {}".format(ab_conflict_num))
