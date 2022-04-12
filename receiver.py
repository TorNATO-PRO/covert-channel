import pandas as pd

# obtain the reference dataframe
reference_df = pd.read_csv('gigachad_playlist.csv')
reference_df = reference_df[~reference_df['Track URI'].str.contains('^spotify:local', regex=True, na=False)]
reference_df.reset_index(inplace=True)
reference_dict = {row['Track URI']: index for index, row in reference_df.iterrows()}

# read the playlist
df = pd.read_csv('amogus.csv').sort_values(by=['Added At'])
decoded_message_list = [chr(reference_dict[row['Track URI']] % 255) for _, row in df.iterrows()]
decoded_message = ''.join(decoded_message_list)

print(decoded_message)
