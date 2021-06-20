topic_config = \
    {
        "music":
            {"switch_on": [
                {"cond": [[[{"pattern": "(\\bpop|popular music|\\brock|\\brap|hip hop|\\bpunk)"}, "user", True],
                           [{"pattern": "(what|which) music do you like"}, "bot", True]],
                          [[{"wiki_parser_types": ["Q488205", "Q36834", "Q177220", "Q753110", "Q105756498",
                                                   "Q215380", "Q207628"]},
                            "user", True],
                           [{"pattern": "(what|which) music do you like"}, "bot", True]],
                          [[{"pattern": "(what|which) (music )?(do )?you (like|enjoy)"}, "user", True],
                           [{"pattern": "(what|which) music do you like"}, "bot", True]]
                          ],
                 "can_continue": "must"}],
             "pattern": "(\\bpop\\b|popular music|\\brock\\b|\\brap\\b|hip hop|\\bpunk\\b)",
             "expected_entities": [{"name": "user_genre", "entity_substr": [["pop", "(\\bpop|popular music)"],
                                                                            ["rock", "(\\brock|\\bpunk)"],
                                                                            ["rap", "(\\brap|hip hop)"]]},
                                   {"name": "user_singer",
                                    "wiki_parser_types": ["Q488205", "Q36834", "Q177220", "Q753110"],
                                    "relations": ["genre", "songs", "albums", "part of"]},
                                   {"name": "user_group", "wiki_parser_types": ["Q105756498", "Q215380"],
                                    "relations": ["genre", "songs", "albums", "has part"]},
                                   {"name": "user_song", "wiki_parser_types": ["Q207628"],
                                    "relations": ["genre", "performer", "part of"]}
                                   ],
             "expected_subtopic_info": [{"subtopic": "discuss_genre",
                                         "cond": [
                                             [{"pattern": "(\\bpop|popular music|\\brock|\\brap|\\btechno|\\bpunk)"},
                                              "user", True]]},
                                        {"subtopic": "discuss_singer",
                                         "cond": [[{"wiki_parser_types": ["Q488205", "Q36834", "Q177220", "Q753110"]},
                                                   "user", True]]},
                                        {"subtopic": "discuss_group",
                                         "cond": [[{"wiki_parser_types": ["Q105756498", "Q215380"]}, "user", True]]},
                                        {"subtopic": "discuss_song",
                                         "cond": [[{"wiki_parser_types": ["Q207628"]}, "user", True]]},
                                        {"subtopic": "my_music",
                                         "cond": [[{"pattern": "(what|which) (music )?(do )?you (like|enjoy)"},
                                                   "user", True]]}],
             "smalltalk": [{"utt": ["Yes, I like {user_genre}!",
                                    "My favourite {user_genre} performer is {[bot_data, user_genre, singer]}.",
                                    "The song {[bot_data, user_genre, song]} is the best!",
                                    "What {user_genre} singers or bands are in your playlist?"],
                            "subtopic": "discuss_genre",
                            "expected_entities": [{"name": "user_singer",
                                                   "wiki_parser_types": ["Q488205", "Q36834", "Q177220", "Q753110"],
                                                   "relations": ["genre", "songs", "albums", "part of"]},
                                                  {"name": "user_group", "wiki_parser_types": ["Q105756498", "Q215380"],
                                                   "relations": ["genre", "songs", "albums", "has part"]},
                                                  {"name": "user_song", "wiki_parser_types": ["Q207628"],
                                                   "relations": ["genre", "performer", "part of"]}],
                            "expected_subtopic_info": [{"subtopic": "discuss_singer",
                                                        "cond": [[{"wiki_parser_types": ["Q488205", "Q36834", "Q177220",
                                                                                         "Q753110"]},
                                                                  "user", True]]},
                                                       {"subtopic": "discuss_group",
                                                        "cond": [[{"wiki_parser_types": ["Q105756498", "Q215380"]},
                                                                  "user", True]]},
                                                       {"subtopic": "discuss_song",
                                                        "cond": [[{"wiki_parser_types": ["Q207628"]}, "user", True]]},
                                                       {"subtopic": "my_music",
                                                        "cond": [[{"pattern": "(what|which) (music )?(do )?you "
                                                                              "(like|enjoy)"},
                                                                  "user", True]]}]},
                           {"utt": ["You have a good taste in music! I also listen to {user_singer}.",
                                    "I'm fascinated with their songs {[user_singer, songs]}."],
                            "subtopic": "discuss_singer",
                            "expected_subtopic_info": [{"subtopic": "pop",
                                                        "cond": [[{"user_info": {"user_genre": "pop"}}, "user", True],
                                                                 [{"entity_triplets": ["user_singer", "genre",
                                                                                       ["pop", "pop music"]]}]]},
                                                       {"subtopic": "rock",
                                                        "cond": [[{"user_info": {"user_genre": "rock"}}, "user", True],
                                                                 [{"entity_triplets": ["user_singer", "genre",
                                                                                       ["rock", "rock music",
                                                                                        "heavy metal"]]},
                                                                  "user", True]]},
                                                       {"subtopic": "rap",
                                                        "cond": [[{"user_info": {"user_genre": "rap"}}, "user", True],
                                                                 [{"entity_triplets": ["user_singer", "genre",
                                                                                       ["rap", "hip hop"]]},
                                                                  "user", True]]},
                                                       {"subtopic": "my_music",
                                                        "cond": [[{"pattern": "(what|which) (music )?(do )?you "
                                                                              "(like|enjoy)"},
                                                                  "user", True]]}
                                                       ]
                            },
                           {"utt": ["You have a good taste in music! I also listen to {user_group}.",
                                    "I'm fascinated with their songs {[user_group, songs]}."],
                            "subtopic": "discuss_group",
                            "expected_subtopic_info": [{"subtopic": "pop",
                                                        "cond": [[{"user_info": {"user_genre": "pop"}}, "user", True],
                                                                 [{"entity_triplets": ["user_singer", "genre",
                                                                                       ["pop", "pop music"]]}]]},
                                                       {"subtopic": "rock",
                                                        "cond": [[{"user_info": {"user_genre": "rock"}}, "user", True],
                                                                 [{"entity_triplets": ["user_singer", "genre",
                                                                                       ["rock", "rock music",
                                                                                        "heavy metal"]]},
                                                                  "user", True]]},
                                                       {"subtopic": "rap",
                                                        "cond": [[{"user_info": {"user_genre": "rap"}}, "user", True],
                                                                 [{"entity_triplets": ["user_singer", "genre",
                                                                                       ["rap", "hip hop"]]},
                                                                  "user", True]]},
                                                       {"subtopic": "my_music",
                                                        "cond": [[{"pattern": "(what|which) (music )?(do )?you "
                                                                              "(like|enjoy)"},
                                                                  "user", True]]}
                                                       ]
                            },
                           {"utt": ["The song {user_song} is very cool!",
                                    "I like listening to {[user_song, performer] music}."],
                            "subtopic": "discuss_song",
                            "expected_subtopic_info": [{"subtopic": "pop",
                                                        "cond": [[{"user_info": {"user_genre": "pop"}}, "user", True],
                                                                 [{"entity_triplets": ["user_singer", "genre",
                                                                                       ["pop", "pop music"]]}]]},
                                                       {"subtopic": "rock",
                                                        "cond": [[{"user_info": {"user_genre": "rock"}}, "user", True],
                                                                 [{"entity_triplets": ["user_singer", "genre",
                                                                                       ["rock", "rock music",
                                                                                        "heavy metal"]]},
                                                                  "user", True]]},
                                                       {"subtopic": "rap",
                                                        "cond": [[{"user_info": {"user_genre": "rap"}}, "user", True],
                                                                 [{"entity_triplets": ["user_singer", "genre",
                                                                                       ["rap", "hip hop"]]},
                                                                  "user", True]]},
                                                       {"subtopic": "my_music",
                                                        "cond": [[{"pattern": "(what|which) (music )?(do )?you "
                                                                              "(like|enjoy)"},
                                                                  "user", True]]}
                                                       ]
                            },
                           {"utt": ["I would like to tell you about some latest pop songs, should I continue?"],
                            "subtopic": "pop",
                            "expected_subtopic_info": [{"subtopic": "pop_more", "cond": [["is_yes", "user", True]]}]},
                           {"utt": [
                               "I would like to tell you about some latest popular rock songs, should I continue?"],
                            "subtopic": "rock",
                            "expected_subtopic_info": [{"subtopic": "rock_more", "cond": [["is_yes", "user", True]]}]},
                           {"utt": [
                               "I would like to tell you about some latest popular rap tracks, should I continue?"],
                            "subtopic": "rap",
                            "expected_subtopic_info": [{"subtopic": "rap_more", "cond": [["is_yes", "user", True]]}]},
                           {"utt": ["Save your tears by The Weeknd and Ariana Grande is a cool track.",
                                    "Do you like Ariana Grande?"],
                            "subtopic": "pop_more"},
                           {"utt": ["BTS song Butter is number one in the chart.",
                                    "What do you think about Korean pop or K-pop?"],
                            "subtopic": "pop_more"},
                           {"utt": ["Noverber Rain by Gunz and Roses is a cool track! Do you like Gunz and Roses?"],
                            "subtopic": "rock_more"},
                           {"utt": ["I also like Nothing Else Matters by Metallica.",
                                    "Lars Ulrich told that they are recording a new album which will be the best in "
                                    "their discography."],
                            "subtopic": "rock_more"},
                           {"utt": [
                               "I did it by DJ Khaled, Post Malone, DaBaby and Megan Thee Stallion is a cool track!",
                               "Do you like the vocal of Post Malone?"],
                            "subtopic": "rap_more"},
                           {"utt": ["I also like Austronaut in the Ocean track of Masked Wolf.",
                                    "I saw a clip for this song Youtube, it is about spaceflight on the Moon."],
                            "subtopic": "rap_more"},
                           {"utt": ["I like Scorpions.", "Wind of Change is the best!"],
                            "subtopic": "my_music"},
                           {"utt": ["I think that live performance of your favourite singer is a cool event.",
                                    "Have you been to any live shows lately?"]},
                           {"utt": ["Do you like to listen music during gaming, while you are playing a game?",
                                    "I can tell you about some music for gaming, should I continue?"],
                            "expected_subtopic_info": [{"subtopic": "gaming_music",
                                                        "cond": [["is_yes", "user", True],
                                                                 [{"pattern": "(continue|tell)"}, "user", True]]}]},
                           {"utt": ["I like gaming music mixes on Youtube.",
                                    "There are drum-n-bass, trap, electro house and dubstep in these tracklists.",
                                    "Would you like to know about some chilling tracks you can listen while gaming?"],
                            "expected_subtopic_info": [{"subtopic": "gaming_music_tracks",
                                                        "cond": [["is_yes", "user", True],
                                                                 [{"pattern": "(continue|tell)"}, "user", True]]}],
                            "subtopic": "gaming_music"},
                           {"utt": ["Vicetone, Ship Wrek, Roy Knox and TheFatRat are top performers!",
                                    "Have a pleasant listening!"],
                            "subtopic": "gaming_music_tracks"}
                           ],
             "bot_data": {"rock": {"singer": "Deep Purple", "song": "Smoke on the Water"},
                          "pop": {"singer": "Drake", "song": "Hotline Bling"},
                          "rap": {"singer": "Travis Scott", "song": "Goosebumps"}},
             "ackn": [{"cond": [[{"pattern": "my favo(u)?rite song is (.*?)"}, "user", True]],
                       "answer": ["I like this song too!"]},
                      {"cond": [[[{"pattern": "live shows"}, "bot", True], ["is_yes", "user", True]]],
                       "answer": ["I'm happy that you had a good time!"]},
                      {"cond": [[[{"pattern": "live shows"}, "bot", True], ["is_no", "user", True]]],
                       "answer": ["There wasn't much going on due to CoVID-19. Hope we will get some in future."]}]
             }
    }