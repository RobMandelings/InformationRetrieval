<delete><query>*:*</query></delete>

http://localhost:8983/solr/chessGames/select?fl=id,name,game_id,score,board&q=board:(Ra1 Ke1 Rh1 Pa2 Pb2 Pf2 Pg2 Ph2 Pc3 Pd3 Qf3 qe5 pc6 Ne6 bg6 pa7 pb7 be7 pg7 ph7 ra8 ke8 rh8)&group=true&group.field=game_id

http://localhost:8983/solr/chessGames/select?fl=id,name,game_id,score,board&q=board:(Ra1%20Ke1%20Rh1%20Pa2%20Pb2%20Pf2%20Pg2%20Ph2%20Pc3%20Pd3%20Qf3%20qe5%20pc6%20Ne6%20bg6%20pa7%20pb7%20be7%20pg7%20ph7%20ra8%20ke8%20rh8)group=true&group.field=game_id