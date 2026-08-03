# psychology-knowledge-atlas — 交接狀態

## ACTIVE WORK

```yaml
phase: P2-SC
unit: forty-eight-target-source-corpus
status: in_progress
base_commit: 593551e
started_at: 2026-07-28
objective: 先為原版48項研究目標完成可恢復、可稽核的來源蒐集，再開始閱讀、建立主張或撰寫內容
active_target: transpersonal-psychology
remaining_targets: [transpersonal-psychology(45), biopsychosocial-model(46), social-psychology(47), health-psychology(48)]
remaining_notes:
  - 一包一 agent、串行不平行；每包獨立 commit + push 後才派下一包，一個 Sonnet agent 約吃 33% 的 Claude 5H 窗
  - health-psychology(48) 最後跑，且用全新隔離 process；醫療／疾病主題詞密集曾在 psychology-schools 觸發 AUP 假陽性連鎖
canonical_inputs:
  - research/targets.json
  - research/source-packs/*.json
target_files:
  - research/source-packs/transpersonal-psychology.json
expected_result: 下一來源包的所有槽位完成搜尋與裁決；合格可讀正文完成私有快取、格式與雜湊稽核；不建立 claims 或 reader prose
boundaries:
  - legacy repo 只提供48項 identity/order seed；不匯入舊文章、摘要或 verdict
  - downloaded 不等於 read/verified/publishable
  - 公開可讀但授權不明全文只進 .private-sources；PDF/EPUB 不進 Git
  - 不繞過登入、付費牆、DRM 或技術存取控制
exit_gate: all 48 packs have recorded searches and slot adjudication; selected retrievable bodies pass MIME/size/hash audit; failures and version boundaries are explicit; validator, full tests and diff checks pass
completed_items:
  - 固定48項及1..48順序，並標記學派／傳統／理論／治療／領域／模型類型
  - 建立48份 source packs、source-pack schema、初始化器、下載器與稽核器
  - source-pack audit PASS；路徑逃逸與 MIME signature regression tests PASS
  - individual-psychology pilot 已完成所有來源槽位初次系統搜尋並標為 audited
  - individual-psychology 已下載並雜湊驗證10筆全文／正式網頁：兩本英文原典版本、一份1912德文原典校對轉錄、歷史／理論／批判／實證／文化及當代延續材料
  - 明示排除一份雖可公開連線、但文件內宣告僅限訂閱者個人使用的 Understanding Human Nature 數位版，待找公版替代
  - structuralism 已 audited：8筆全文／正式網頁，涵蓋Wundt德文原典與英譯、Titchener原典、方法、批判、歷史轉折及機構延續邊界
  - functionalism 已 audited：8筆全文／正式網頁，涵蓋James兩卷、Dewey、Angell、Calkins、早期實驗、歷史轉折及APA當代學科定義
  - 精神分析傳統批次新增6包 audited、38筆實際正文／正式網頁：psychoanalysis 7、analytical-psychology 7、neo-freudian 6、object-relations 6、ego-psychology 6、self-psychology 6
  - 六包均分開原典／方法、歷史、批判、實證與當代機構角色；寬泛的psychodynamic療效研究不冒充特定分支理論驗證
  - 移除NYPL回傳的212-byte防機器人空頁並以International Erich Fromm Society正式頁替代；兩筆403全文端點亦以可讀全文替代，沒有保留摘要充數
  - 第二個大批次完成6包 audited、37筆實際正文／正式網頁：behaviorism 7、social-learning-theory 7、gestalt-psychology 6、gestalt-therapy 6、humanistic-psychology 6、existential-psychology 5
  - 學派與治療分支保持分離：Gestalt心理學的知覺研究不冒充Gestalt治療療效；社會學習理論與後期社會認知理論保留版本邊界；存在治療的窄範圍meta-analysis不升格為整個存在心理學的驗證
  - 移除3筆APA Incapsula防機器人空殼並以AHP正式歷史／現況頁替代；修正錯誤PMC識別與書目資料；Skinner Foundation明示個人使用、不得轉傳的數位本列為excluded且不快取
  - 目前15/48來源包 audited、累計101筆實際正文／正式網頁；跨包相同正文依SHA-256辨識，不當成不同來源正文灌水
  - 第三個大批次完成5包 audited、36筆實際正文／正式網頁：person-centered-therapy 7、cognitive-psychology 7、cbt 9、biological-psychology 6、evolutionary-psychology 7
  - 下載後辨識並移除2份3 KB防機器人假頁面，替換4個403／TLS失敗端點；另把生物心理學的書目／目錄頁升級成27.7 MB開放教科書全文與11.2 MB Hebb 1949原典全文
  - 個人中心治療補入西語歷史研究；CBT補入文化調適meta-analysis與自助式網路CBT惡化風險研究；不以一般醫療的person-centred care冒充person-centred therapy
  - 認知心理學與跨領域cognitive science、生物心理學與neuroscience、演化心理學與廣義human behavior and evolution均保留範圍邊界
  - 目前20/48來源包 audited、累計137筆實際正文／正式網頁；本批36筆逐一通過大小、MIME、SHA-256、假頁面與批內重複檢查
  - 第三波批次完成5包 audited、31筆實際正文／正式書目頁：dbt 6、act 6、mbct 7、mbsr 6、rebt 6；其中29個唯一 landing URLs，兩份跨包共用的 mindfulness meta-review／harm framework 不冒充獨立來源
  - DBT 1991 與 MBSR 1982 原始研究的出版社全文未取得；前者改存 NCBI E-utilities 官方摘要 XML，後者存 PubMed 正式摘要頁，兩者均明示不算全文閱讀
  - 移除一份 HTTP 成功但實際為 Google reCAPTCHA challenge 的 DBT 假頁面；替代 XML 的 PMID、題名、摘要與 DOI 已核對，其他 captcha 字樣只出現在正常頁面的表單腳本
  - ACT 與 REBT 的安全／文化槽位搜尋後沒有找到足以通過本輪取得門檻的專屬來源，明記 searched_no_qualifying_source，不以一般 CBT／正念材料或搜尋摘要填補
  - 目前25/48來源包 audited、累計168筆實際正文／正式書目頁；本批全部通過大小、MIME、SHA-256、私有快取路徑、假頁面檢查，canonical validator 與完整77 tests PASS
  - constructivist-psychotherapy 已 audited：6筆正文／正式網頁；其中 ERIC 與 Open Library 只保存摘要／書目頁，不冒充全文，另有3份開放研究全文與1個當代專業網絡正式頁
  - 建構主義心理治療家族、personal construct therapy、敘事／對話取向保持範圍邊界；特定纖維肌痛女性樣本的主動比較試驗不升格為整個家族的療效結論
  - safety/guidelines 與 cultural/language context 已搜尋但本輪無合格專屬來源，明記 searched_no_qualifying_source；6筆快取均通過大小、MIME、SHA-256與假頁面檢查
  - 目前26/48來源包 audited、累計174筆實際正文／正式書目頁
  - narrative-therapy 已 audited：7筆正文／正式書目頁，涵蓋Dulwich創始史、White與Epston 1990原典書目、方法說明、早期獨立批評、質性／混合研究綜整、飲食疾患結果回顧及當代機構延續
  - White–Epston narrative therapy 與 narrative exposure therapy、narrative medicine、generic storytelling interventions 保持範圍邊界；療效回顧的特定診斷與研究設計限制不升格為一般療效結論
  - 一份Aboriginal community協作實務報告因PDF內明文限制儲存／傳播而列為excluded且不快取；另一份文化調適回顧因研究的是不同的Narrative Exposure Therapy而排除
  - safety/guidelines 與 cultural/language context 均完成搜尋但本輪無可快取的合格專屬來源；7筆取得物通過大小、MIME、SHA-256、題名與假頁面檢查
  - 目前27/48來源包 audited、累計181筆實際正文／正式書目頁
  - sfbt 已 audited：8筆正文／正式書目頁，涵蓋參與者歷史、de Shazer 1985 原典書目、SFBTA 2025方法手冊、獨立批判摘要、umbrella review正式摘要、癌症臨床結果meta-analysis、伊朗區域meta-analysis及當代專業協會延續
  - SFBT與generic brief therapy、strength-based practice及只借用solution-focused技巧的介入保持範圍邊界；癌症與伊朗特定證據不升格為普遍療效或跨文化適用結論
  - 一個Deep Blue端點回傳1.9 KB Angular空殼而移除；另有出版社PDF 403、UvA全文兩次逾時及CRD主機TLS驗證失敗，均改用正式PubMed／Europe PMC／NCBI來源，沒有繞過存取或TLS防護
  - safety/guidelines 已搜尋但無合格專屬來源；8筆取得物通過大小、MIME、SHA-256、題名、XML解析與假頁面檢查
  - 目前28/48來源包 audited、累計189筆實際正文／正式書目頁
  - transactional-analysis 已 audited：10筆正文／正式書目或摘要頁，涵蓋Berne檔案史、1961原典書目、早期原文重刊摘要、ITAA核心概念、獨立博士論文建構檢驗、聚焦研究回顧、探索性meta-analysis、EATA倫理規範、西語系統回顧及當代國際協會延續
  - 溝通分析的心理治療／人格理論與金融交易分析、語言學transaction analysis、一般溝通訓練及只引用TA的整合治療保持範圍邊界；探索性meta-analysis跨設計、族群、學派與結果的合併效果不升格為特定適應症療效
  - 1983建構效度出版社頁回傳403，改存Utah State正式論文摘要；PMC PDF端點回傳1.8 KB proof-of-work空殼，移除後保留Europe PMC正式摘要XML並明示不是全文，沒有繞過存取控制
  - 10筆取得物通過大小、MIME、SHA-256、題名、PDF文字、XML解析與假頁面檢查；西語回顧補足語言版本邊界，但不冒充文化調適證據
  - 目前29/48來源包 audited、累計199筆實際正文／正式書目或摘要頁
  - reality-therapy 已 audited：8筆正文／正式書目或摘要頁，涵蓋WGI創始史、Glasser 1965原典書目、Wubbolding WDEP方法、獨立教育實施批判、WSIPP特定親職方案記錄、土耳其青年系統回顧、韓國青少年meta-analysis及當代國際組織延續
  - Reality Therapy／Choice Theory與virtual-reality exposure therapy、reality orientation、reality testing及一般choice／responsibility介入保持範圍邊界；教育、親職、青年團體與韓國自尊結果不升格為一般臨床療效
  - Wiley方法章回傳Cookies Turned Off錯誤殼，移除後改存ERIC正式會議論文全文；safety/guidelines搜尋後無可公開檢查的專屬 adverse-event／contraindication指引，沒有把WGI自述的ethics standards冒充安全證據
  - 8筆取得物通過大小、MIME、SHA-256、題名、PDF文字與假頁面檢查；土耳其與韓語來源保留語言、地域、族群及結果邊界
  - 目前30/48來源包 audited、累計207筆實際正文／正式書目或摘要頁
  - social-constructionism 已 audited：8筆正文／正式書目或摘要頁，涵蓋SEP獨立概念邊界、Berger與Luckmann 1966原典書目、Gergen 1985心理學綱領正式摘要、巴西葡語理論回顧、Hacking獨立批判書目、當代社會心理學應用、南美去殖民研究及Taos Institute延續
  - 社會建構論與Piaget式social constructivism、constructivist psychotherapy及泛稱「constructed」的研究保持範圍邊界；單一社會類別或地方應用的研究不升格為整套異質後設理論的實證驗證
  - Nature端點回傳3 KB Client Challenge空殼，移除後改存作者網站完整PDF；USP PDF端點逾時，改用同DOI的SciELO官方PDF，Gergen舊全文連結404則只保留Swarthmore正式摘要頁，均未繞過存取控制
  - 8筆取得物通過大小、MIME、SHA-256、題名、PDF文字與假頁面檢查；葡語與巴西地方研究保留語言、地域、方法及知識主權邊界
  - 目前31/48來源包 audited、累計215筆實際正文／正式書目或摘要頁
  - cultural-historical-psychology 已 audited：9筆正文／正式書目或摘要頁，涵蓋Kharkov學派修正史、Vygotsky 1962英譯書目與俄文原典重刊、百年理論方法綜述、revisionist論集及其批判回應、Vygotsky-Sakharov方法重做、俄文至葡語版本比較與當代專業期刊延續
  - Vygotsky本人的文化—歷史理論、Kharkov後繼研究、Leontiev／Engeström活動理論、廣義sociocultural learning、scaffolding與social constructivism保持範圍邊界；197名莫斯科學童的單一方法研究不升格為整個學派的實證驗證
  - PubMed回傳reCAPTCHA頁，改用Europe PMC core XML；並由正式紀錄抓出候選Springer DOI錯誤，修正為APA DOI 10.1037/1093-4510.11.2.101，未繞過技術控制
  - 俄文重刊PDF可視閱讀但舊字型編碼造成自動抽字亂碼，已明記readability邊界；其餘取得物通過大小、MIME、SHA-256、題名、PDF文字、XML解析與假頁面檢查
  - 目前32/48來源包 audited、累計224筆實際正文／正式書目或摘要頁
  - multicultural-feminist-therapy 已 audited：9筆正文／正式書目或摘要頁，涵蓋1970年代早期綱領、Brown參與者原典書目、多元女性方法章、階級與族群交織批判、實證整合回顧、APA女性實務指南、Feminist Therapy Institute倫理規範、印尼系統文獻回顧及當代網絡延續
  - 多元文化／女性主義治療視為異質 therapy family，不與一般女性心理治療、女性樣本、empowerment介入、relational-cultural therapy或泛稱gender-sensitive care等同；整個家族的專屬臨床結果統合搜尋後無合格來源，明記 searched_no_qualifying_source
  - APA頁面回傳212-byte Incapsula空殼、Library of Congress端點回傳724-byte JavaScript殼、Taylor & Francis與ScienceDirect回傳403，均移除或改用Open Library／Crossref正式紀錄，並修正一筆原先指向無關文章的錯誤DOI，未繞過技術控制
  - cross-cultural-psychology 已 audited：9筆正文／正式書目或摘要頁，涵蓋JCCP 1970與IACCP 1972領域史、1966跨文化視知覺奠基研究書目、領域教科書與方法綱領、WEIRD與去殖民批判、Many Labs 2跨36國／地區大型重複研究、ITC測驗調適準則及當代國際協會延續
  - 跨國取樣不自動等於跨文化研究，翻譯不自動等於測量等值，群體平均不外推成個人或國家固定特質；cross-cultural psychology與cultural psychology、indigenous psychology及intercultural communication保留邊界
  - Harvard全文端點回傳403後改存UBC正式作者摘要頁；Many Labs 2取得101頁LSE repository manuscript，ITC準則取得41頁PDF；正常IACCP頁面雖含表單reCAPTCHA設定字串，但正文與題名完整，不是challenge殼
  - 目前34/48來源包 audited、累計242筆實際正文／正式書目或摘要頁；本批18筆均通過大小、MIME、SHA-256、題名／PDF文字與假頁面人工判讀
  - systems-family-therapy 已 audited：10筆正文／正式書目頁，涵蓋葡語領域史、Bowen與Minuchin兩支原典書目、SAMHSA方法章、性別權力批判、兒童與成人問題證據回顧、難民家庭介入綜整、AAMFT倫理規範及當代專業協會延續
  - 系統／家庭治療保持 therapy family 邊界：Bowen、結構、策略、Milan、行為、solution-focused與multisystemic模式不視為單一標準療程；廣泛child review內的parent training與parent-implemented behavioral programmes不冒充所有家庭治療分支的共同證據
  - Wiley兩個端點回傳403，改存Crossref正式書目紀錄且不把文章正文當成已讀；AAMFT倫理規範處理多重當事人、同意、保密與權力，但不冒充adverse-event review或取代地方法律
  - attachment-theory 已 audited：8筆正文／正式書目頁，涵蓋Bretherton歷史紀錄、Bowlby與Ainsworth原典書目、當代理論綜整、跨文化普遍性批判、CATS個體資料統合計畫、納入西／葡語的拉丁美洲回顧及SEAS當代延續
  - 依附理論保持測量與應用邊界：嬰兒Strange Situation、Adult Attachment Interview與成人浪漫依附自陳量表不互換；依附理論不等同attachment parenting、reactive attachment disorder、generic bonding或具爭議的強制性attachment therapy，統計關聯亦不作個人診斷或決定論預測
  - SUNY作者PDF因TLS主機憑證不符而改存INIST-CNRS正式書目紀錄；CATS的PMC端點回傳Google reCAPTCHA空殼，移除後改存UCL repository的8頁正式版本，均未停用憑證驗證或繞過技術控制
  - 目前36/48來源包 audited、累計260筆實際正文／正式書目或摘要頁；本批18筆通過大小、MIME、SHA-256、題名／PDF文字與假頁面人工判讀
  - art-therapy 已 audited：9筆正文／正式書目頁，涵蓋英國專業史、Naumburg原典書目、AATA範圍定義、NIHR量化與質性綜整、2024跨適應症RCT meta-analysis、AATA倫理規範、難民兒少證據回顧及當代協會延續
  - art therapy與arts-in-health、休閒藝術、藝術教育、成人著色及泛expressive arts programmes保持邊界；2024綜整中81%分析結果無效果且整體研究品質低，難民兒少回顧亦判為證據不足，不把探索性合併效果升格為普遍療效
  - play-therapy 已 audited：9筆正文／正式書目頁，涵蓋獨立歷史章紀錄、Axline 1947原典書目、方法與分支概覽、智力障礙族群機制回顧、CCPT meta-analysis、創傷兒少回顧、PTI倫理框架、加拿大原住民族文化批判及UNT當代研究中心
  - play therapy與一般遊戲、教育性遊戲、hospital therapeutic play、filial therapy、Theraplay、sandplay及泛play-based intervention保持邊界；CCPT、directive與其他理論分支不視為同一療程，加拿大文章不把First Nations、Métis與Inuit合成單一文化
  - APT最佳實務PDF與About頁均回傳403，分別改存Play Therapy International可讀倫理框架與University of North Texas正式研究中心頁，保留失敗原因且未繞過存取控制
  - psychodrama 已 audited：9筆正文／正式書目頁，涵蓋80年計量史、Moreno多卷原典書目、FEPTO方法說明、2019與2025方法批判綜整、中國RCT meta-analysis、FEPTO倫理規範、葡／英／西語巴西回顧及ASGPP當代延續
  - psychodrama與drama therapy、sociodrama、一般角色扮演、模擬訓練及嵌入其他治療的role-playing techniques保持邊界；近期研究仍缺較多RCT／準實驗，跨族群與跨模型的正向敘述不冒充單一通用效果
  - music-therapy 已 audited：9筆正文／正式書目頁，涵蓋英國醫療史方法、Alvin 1966原典書目、AMTA／CBMT方法範圍、術語與報告品質批判、精神醫療meta-review、autistic people之Cochrane review、AMTA倫理規範、文化中心實務批判及WFMT當代延續
  - 音樂治療與一般聽音樂、music medicine、arts-in-health、sound healing保持邊界；credentialed delivery只界定專業角色，不自動指定技術或證明療效，跨診斷與特定族群綜整亦不升格為通用效果
  - indigenous-psychology 已 audited：7筆正文／正式書目或摘要頁，涵蓋多國起源調查、2006參與者論集、楊國樞三種心理學與華人實證成果紀錄、Jahoda外部批判、當代國際網絡及CARE資料治理原則
  - 本土心理學保持複數傳統與知識主權邊界：不把Sikolohiyang Pilipino、華人／臺灣、Māori、印度、韓國等地方運動合成單一文化，也不把indigenous psychologies等同於所有關於Indigenous Peoples的研究；CARE只處理資料治理，不冒充完整心理學研究倫理碼
  - morita-therapy 已 audited：8筆正文／正式書目頁，涵蓋1920至30年代日本社會史、森田正馬1928日文原典紀錄、日英門診指引、百年版本回顧、英國適應性pilot RCT、Cochrane焦慮綜整、跨文化改編及日本森田療法學會延續
  - 古典住院四階段、後期對話式門診、英國8至12節改編與Constructive Living保持邊界；Cochrane納入研究小、偏差風險高且不良事件報告不足，安全／禁忌專屬來源搜尋後無合格材料，明記searched_no_qualifying_source
  - Springer兩個不同文章端點回傳同一3 KB Client Challenge殼，均移除並改存PMC正文與德國國家圖書館PDF；AIATSIS PDF與頁面403後以CARE原始論文補資料主權邊界，SAGE批判文章403後只存Crossref正式DOI紀錄，未繞過技術控制
  - 目前42/48來源包 audited、累計311筆實際正文／正式書目或摘要頁；本批24筆通過大小、MIME、SHA-256、題名、PDF文字、假頁面與批內重複檢查
  - naikan-therapy 已 audited：12筆正文／正式書目或摘要頁，涵蓋維也納大學宗教學獨立專章與竹元隆洋日本學會史、吉本伊信1957與1975原典NDL紀錄、川原隆造方法論、Ozawa-de Silva世俗化批判、田代等長期憂鬱摘要與Qian等唾液oxytocin／cortisol研究、Zhang等思覺失調症輔助RCT、日本内観学会認定制度與沿革、榛木美恵子國際化日文研究
  - naikan與morita-therapy分屬獨立目標，未共用任一來源；亦與一般感恩練習、正念、慈心與西方自我反思材料保持邊界。淨土真宗「身調べ」與吉本世俗化「内観」分開登錄（竹元含兩者對照表、Pokorny記明身調べ知識僅來自吉本本人陳述）；集中內觀（一週、每日約15小時）與日常／分散內觀分開，兩項成效研究皆為中國改編式給予（Zhang為20次×2小時住院輔助、Qian為連續5天），不當作日本一週住宿式內觀的證據
  - 安全／禁忌槽位標 searched_no_qualifying_source：日本内観学会1995倫理規程只有責任、秘密保持與利益衝突，無不良事件、篩選或中止協定；日文禁忌說法只溯及無引用的百科段落與商業機構頁；精神神経学雑誌2019全文須登入
  - 牛津研究百科Chilson條目的公開PDF自帶「Subscriber: OUP-Reference Gratis Access／Personal use only」限制，刪除快取改標 excluded；改用的Crossref unixref transform雖回200但無Content-Type，collector無法歸類故一併標 excluded，最後以維也納大學自存專章（Religion in Austria vol.6, pp.161–218）補獨立學術身分；oxfordre landing導向Cloudflare未繞過
  - 日本内観学会一個4.8 KB近空頁移除，改存認定制度與沿革兩頁；WebFetch對日文頁摘要曾杜撰刊名與年份，改以urllib取原始位元組並以shift_jis解碼核對
  - 目前43/48來源包 audited、累計323筆實際正文／正式書目或摘要頁；本包12筆通過大小、MIME、SHA-256、題名、PDF文字（pypdf）、假頁面與包內重複檢查
  - positive-psychology 已 audited：18筆正文／正式書目或摘要頁，涵蓋Froh 2004優先權史與Ryff 2022外部回顧、Seligman與Csikszentmihalyi 2000創刊綱領、Peterson與Seligman 2004 VIA手冊書目、Fredrickson broaden-and-build與Butler／Kern PERMA-Profiler、Waterman人本／正向分裂分析與van Zyl等2024批判系統回顧、Coyne與Tennen癌症照護批判摘要、White等PPI效果量重估、Brown／Sokal／Friedman critical positivity ratio數學駁斥、Fredrickson與Losada 2005更正紀錄、Lim與Tierney對照活性治療綜整、IPPA與2023計量學現況、非西方PPI meta-analysis、Fernández Ríos西語批判與非洲wellbeing回顧
  - 正向心理學與人本心理學保持爭議史邊界：Maslow 1954已用該詞、Froh主張優先權、Waterman記錄兩者哲學分歧，一律登錄為爭議歷史而非既定血緣，且與已 audited 的 humanistic-psychology 包零來源重疊；亦與正向思考、自助、快樂產業及勵志文學分離（pursuit-of-happiness.org、positivepsychology.com、sessionlab、bartleby 等教練／自助頁全數排除，未當研究或批判證據）；Diener系subjective wellbeing泛論不冒充本subfield，PERMA、VIA、broaden-and-build以框架身分登錄不等同整個subfield；second-wave PP／PP 2.0 已搜尋但Wong全部落在T&F／Routledge／Springer或作者推廣站，無合格開放正文故未納入
  - empirical_status 刻意納入方法學批判而非只收有利meta-analysis：White等2019重估PPI效果量遠小於原估、Brown等2013以arXiv預印本駁斥critical positivity ratio的數學基礎、Fredrickson與Losada 2005經PubMed ErratumIn（Am Psychol 2013;68(9):822）與5筆CommentIn正式記錄部分撤稿、Lim與Tierney以活性對照治療檢驗憂鬱PPI；每筆身分皆以實際檢索核對而非憑記憶
  - 三筆因權利或存取限制標 excluded 且不快取：Annual Review的Seligman 2019自述PDF帶「Access provided by University of Pennsylvania／For personal use only」訂閱者浮水印，1998 APA會長演說掃描本帶APA「solely for the personal use of the individual user and is not to be disseminated broadly」邊註，兩份已下載正文均刪除只留引用指標；Cabanas 2018在SAGE與MPG.PuRe皆403，僅存DOI指標，其意識形態批判改由van Zyl等系統回顧承擔。替代候選同因權利否決：UPenn站上的Seligman與Pawelski 2003 FAQs是帶「All use subject to about.jstor.org/terms」的JSTOR列印本，Park等2006五十四國研究是帶訂閱大學與下載日期戳記的T&F機構下載本；改採開放取用的Ryff 2022 Frontiers回顧。Oxford Academic的Coyne與Tennen全文403後改存NCBI E-utilities官方摘要XML並明記不算全文
  - 目前44/48來源包 audited、累計341筆實際正文／正式書目或摘要頁；本包18筆通過大小、MIME、SHA-256、題名、PDF文字（pypdf）、假頁面、權利浮水印全檔regex掃描與包內重複檢查
next_action: 依 research/targets.json 順序從 transpersonal-psychology 開始，繼續採每批2至3項處理其餘4項，不建立正文。非英語只在原始語言、地方傳統或翻譯／版本差異影響正確性時補，不設配額
```

## P3-S COMPLETION RECORD

```yaml
phase: P3-S
unit: indigenous-psychology-seven-question-pilot
status: validated
base_commit: 926b297
started_at: 2026-07-27
target_entity: indigenous-psychology
objective: 以來源、原子 claim、evidence 與 relation 完成第四個學派 pilot；明確保護文化差異、Indigenous leadership 與資料／知識主權邊界
candidate_questions:
  - S1 name-region-scope-polysemy
  - S2 plural-histories-and-local-movements
  - S3 worldview-self-relations-community-context
  - S4 epistemology-methods-language-research-relationship
  - S5 primary-bibliography-organizations-versions
  - S6 coloniality-ethics-data-knowledge-sovereignty
  - S7 cross-cultural-cultural-local-tradition-relations
completed_items:
  - 固定 S1-S7 問題清單；區分 indigenous psychologies 方法論傳統、特定 Indigenous Peoples 與華語「本土心理學」的多義性
  - baseline：validator PASS；60 tests PASS；工作樹起始無重疊改動
  - 來源策略：2006 Indigenous and Cultural Psychology 全文處理概念／歷史／方法；AIATSIS Code 處理研究倫理；CARE 原始論文處理資料主權
  - S1-S7 共完成 26 筆 verified/publishable 原子 claims 與 26 筆 fulltext_direct evidence；每筆有繁中敘述、locator、25 字內短引文與 scope_note
  - S1：明確分開 plural indigenous psychologies 方法論傳統與針對特定 Indigenous Peoples 的研究；華語「本土心理學」保留多義警告
  - S2：保留 1960 年代末多地運動、1970 年代初 Sikolohiyang Pilipino 與 Santiago 1975 fieldwork 三個不同尺度，不建立單一起源神話
  - S3：分開 contextual universals、文化衍生參照框架與 self／relations／environment 分析面向；文化概念不因命名即獲驗證
  - S4：分開 indigenization from without／from within，保留方法多元、參與者語言／福祉／研究關係及不可直接跨文化移植邊界
  - S5：1993 volume、2000 article、2006 edited volume 三筆書目身份分開；後期綜整不回填早期文本
  - S6：以 AIATSIS 固定 self-determination、leadership、benefit、accountability；以 CARE 固定 Collective Benefit、Authority to Control、Responsibility、Ethics 及 FAIR 不充分邊界
  - S7：新增 cross-cultural-psychology 與 sikolohiyang-pilipino identities；建立兩筆 evidence-backed branch_of relations，零 alias/equivalence
  - reader preview：views/specs/indigenous-psychology.json 生成七節、26 claims、2 relations 的繁中 Markdown 與 JSON dossier
  - tests：新增三項 Indigenous psychology regression；完整 suite 63 tests PASS；validator、reader build、git diff --check PASS
  - MAP freshness：本專案原先唯一 drift 是 MAP 未明列既有 build_views.py；本次已補入結構導航；全 workspace 仍有其他專案既存 drift，不屬本任務
next_action: P3-S 四個 bounded pilots 已關閉；下一 gate 是 P4 views，開始前先固定第一個跨 pilot view 的讀者問題、輸入集合與退出門檻
exit_gate: complete — Indigenous psychology S1-S7 7/7 adjudicated; 26 claims and 2 relations use readable direct evidence; cultural, people, context-domain and data-sovereignty boundaries have executable tests; legacy prose/verdict import remains zero; validator, reader build and 63 tests pass
stop_rule: 不把 indigenous psychologies 自動等同「研究 Indigenous Peoples」；不把各民族合成單一文化；任一來源無法讀取就留在 citation/queue 層；不得用搜尋 snippet 補全文
```

## P2-E COMPLETION RECORD

```yaml
phase: P2-E
status: validated
started_at: 2026-07-22
targets:
  - phenomenon entity contract
  - controlled phenomenon_kind and reference-system system_role vocabularies
  - explicit roles for all existing reference systems
  - first named-phenomenon candidate universe (cognitive-bias discovery seed)
  - P2-E pilot phenomena outside cognitive biases registered (misattribution of arousal, broken windows)
  - P2-E evidence source routing for the three pilots: popular / research / critique claims per pilot, each with a source and metadata-only evidence, all publishable:false
validation:
  - canonical validator baseline PASS
  - 32 foundation and P1/P1-E system tests PASS
  - git diff whitespace gate PASS
  - APA CoA C-5 P snapshot: 11/11 candidates adjudicated
  - ANZSRC 2020 FoR Division 52 group slice: 6/6 candidates adjudicated
  - ANZSRC 2020 FoR Division 52 field inventory: 36/36 registered and resolved; 28 included; 2 merged; 6 excluded; 0 pending
  - ANZSRC field group 5203: 4/4 substantive candidates adjudicated; 520399 NEC residual excluded
  - ANZSRC field group 5204: 6/6 substantive candidates adjudicated as research-field identities; 520499 NEC residual excluded
  - ANZSRC field group 5205: 5/5 substantive candidates adjudicated; 520599 NEC residual excluded
  - IAAP active divisions: 18/18 candidates registered and resolved; 12 included; 4 merged; 2 excluded; 0 pending
  - ANZSRC Division 45 Indigenous studies groups: 20/20 registered and resolved; 19 context domains included; 4599 residual excluded; 0 pending
  - context_domain entity type added to distinguish contextual axes from psychology subfields
  - Division 45 groups 4501–4506: 6/6 included as Aboriginal and Torres Strait Islander context domains
  - Division 45 groups 4507–4512: 6/6 included as Māori context domains; te reo Māori canonical names preserved
  - Division 45 groups 4513–4518: 6/6 included as Pacific Peoples context domains
  - Division 45 group 4519: included as a global Indigenous data, methodologies and studies context domain
  - corrected ABS 2025 labels: 4517 Pacific Peoples society and community; 4518 Pacific Peoples sciences
  - phenomenon contract: controlled kind, optional Chinese label, and non-empty resolvable domain_entity_ids
  - reference-system role contract: canonical taxonomy, specialist index, discovery seed, or popular-language inventory
  - wikipedia-cognitive-biases-core discovery seed: 23/23 candidates registered, resolved and included as phenomenon identities; complete:true, resolved:true, pending 0
  - cognitive-bias slice is a bounded discovery seed, NOT the exhaustive ~210-entry source list; complete here means every DECLARED candidate is adjudicated, not that the cognitive-bias universe is exhausted
  - named-effects-routing-pilot discovery seed: 2/2 candidates (misattribution of arousal 吊橋效應, broken windows 破窗效應) registered, resolved and included; complete:true, resolved:true, pending 0
  - three P2-E routing pilots now all have identities: Dunning-Kruger (under the cognitive-bias seed), misattribution of arousal, and broken windows
  - no evidence claims created: every phenomenon is status retrieved, publishable:false, provenance reference_system; identity-only registration
  - entity-types vocabulary now matches validator and includes context_domain plus phenomenon
  - clean GitHub clone at 5faead9 + validator + 19 tests PASS
  - clean GitHub clone at 7e2c41f + validator + 20 tests PASS
  - clean GitHub clone at 6cc662d + validator + 21 tests PASS
  - clean GitHub clone at cd3d1f6 + validator + 22 tests PASS
  - P2-E: 7 new source records registered from search-confirmed identifiers only; where no DOI was confirmed (kruger-dunning-1999, gignac-zajenkowski-2020, wilson-kelling-1982, harcourt-ludwig-2006) identifiers left empty rather than guessed
  - P2-E: 9 claims + 9 evidence records for the three pilots; each pilot has exactly one popular (definition), one research (finding or mechanism), and one critique claim as distinct atomic records, not one blended verdict
  - P2-E: every claim status retrieved, publishable:false, provenance source_derived, with a scope_note bounding overreach; every evidence evidence_level metadata_only, publishable:false, bidirectionally linked to its claim
  - P2-E: access_status recorded honestly (paywalled_unread / publicly_readable_license_unclear / open_fulltext); no full text was read this session, so no fulltext evidence is asserted and nothing is publishable or verified
  - 33 foundation and P1/P1-E/P2-E system tests PASS (added test_p2e_pilot_evidence_routing_is_identity_only)
  - clean GitHub clone at 982ce96 + validator + 33 tests PASS
  - publish/verification gate defined and codified: per-claim_type verified conditions written into CLAUDE.md (popular stays documented framing, research/attribution/mechanism/critique require fulltext + locator + verbatim short_quote); Wikipedia confined to discovery_seed + popular framing in CLAUDE.md and MAP
  - validator strengthened: publishable evidence now requires a non-empty verbatim short_quote, and a publishable claim now requires at least one linked publishable evidence record (closes the metadata-backed-publish loophole)
  - 34 tests PASS (added test_publish_gate_requires_readable_fulltext_with_quote)
  - clean GitHub clone at d5a5311 + validator + 34 tests PASS
  - FIRST worked promotion done: c-dk-popular upgraded end-to-end to status verified + publishable:true via a genuinely fetched Wikipedia lead quote; ev-dk-popular is now fulltext_direct with a verbatim short_quote and a specific locator (Lead section, opening definition sentence). This is a documented-popular-framing claim, not an "effect is real" claim
  - honest no-fulltext case registered alongside it: nuhfer-etal-2017-numeracy (open-access critique, DOI 10.5038/1936-4660.10.1.4) registered as access_status open_fulltext, but its PDF body returned 403 to the fetch tool this session, so c-dk-critique-noise + ev-dk-critique-noise stay abstract_only, publishable:false — a queued citation, deliberately NOT a faked read
  - Dunning-Kruger now spans all three layers on purpose: c-dk-popular (published), c-dk-research + c-dk-critique + c-dk-critique-noise (honest citation/queue), demonstrating tiering rather than uniform verdicts
  - source-prioritization + three-layer policy codified in CLAUDE.md (open replication/meta-analysis first, textbooks/handbooks next, paywalled originals last and allowed to stay metadata_only forever); no-fulltext produces a queued record, not garbage
  - reworked test to test_p2e_pilot_evidence_routing_and_first_promotion: asserts all base claims stay publishable:false EXCEPT c-dk-popular, checks the promoted popular claim + evidence, and pins the Nuhfer no-fulltext honest case
  - 34 tests PASS (test renamed/reworked, no net count change)
  - FIRST research-tier verified claim done: c-anchoring-manylabs-replication (claim_type finding, subject anchoring-bias) promoted through the gate from an openly readable multi-lab replication. Source klein-etal-2014-many-labs (Many Labs 1, Klein et al. 2014, Social Psychology 45(3):142-152, DOI 10.1027/1864-9335/a000178, Hogrefe OpenMind open-access license) full text was read this session: Hogrefe returned 403, but the openly hosted PDF (stanford.edu/~knutson/jdm/klein14.pdf) was fetched and its body extracted with pypdf; abstract, Table 2 and the 'Variation Across Samples and Settings' section were read directly
  - ev-anchoring-manylabs-replication is fulltext_direct with a verbatim short_quote naming anchoring among the "very large effects", locator "Results, 'Variation Across Samples and Settings' subsection, p. 149"; claim scope_note bounds it to a replication finding (Table 2 d approx 1.17-2.42, all p<.001), not a mechanism claim
  - 35 tests PASS (added test_first_research_tier_verified_claim)
exit_gate: satisfied — three pilot routes complete; popular and research fulltext publication paths exercised; honest no-fulltext queue path exercised; dedicated executable test added
next_gate: P3-S structuralism seven-question pilot; begin with S1 identity-time-scope
```

## P2-E progress

- P2-E routes evidence for the three pilots (`misattribution-of-arousal` 吊橋效應, `dunning-kruger-effect` 達克效應, `broken-windows-effect` 破窗效應) into three distinct atomic claims each: a `popular` claim (`claim_type: definition`) recording how the effect is described in popular language, a `research` claim (`finding`, or `mechanism` for broken windows) tied to the primary source, and a `critique` claim (`critique`) tied to a documented non-replication or methodological objection. Popular, research and critique are separate records so a popular framing can never masquerade as a research verdict.
- Every P2-E claim carries a `scope_note` that bounds overreach (single study, US undergraduate sample, contested criminological claim, statistical-artefact objection, etc.), status `retrieved`, `publishable:false`, provenance `source_derived`. Every claim links exactly one evidence record, and each evidence record backlinks its claim (validator enforces the backlink).
- Seven new sources were registered from search-confirmed identifiers only: `dutton-aron-1974-bridge` (DOI + PMID), `kenrick-cialdini-linder-1979` (DOI), `kruger-dunning-1999`, `gignac-zajenkowski-2020`, `wilson-kelling-1982-broken-windows`, `harcourt-ludwig-2006`, and `wikipedia-dunning-kruger-effect`. Where no DOI was confirmed, `identifiers` is left empty rather than guessed. Popular claims reuse the existing Wikipedia article sources for the bridge and broken-windows effects.
- P2-E initially wrote all 9 claims as `metadata_only`, `publishable:false`; the publish gate was then exercised for real. `c-dk-popular` became the atlas's first `verified` + `publishable:true` claim by fetching the live Wikipedia Dunning-Kruger lead and recording its opening definition sentence as a verbatim `short_quote` at a specific locator; `ev-dk-popular` is now `fulltext_direct`. This is a documented-popular-framing claim (`claim_type: definition`), never an assertion that the effect is real.
- The honest no-fulltext path was demonstrated in the same session: `nuhfer-etal-2017-numeracy` (open-access noise/graphical-convention critique, DOI 10.5038/1936-4660.10.1.4, CC BY-NC 4.0) is registered as `access_status: open_fulltext` because that is its license status, but the PDF body returned 403 to the fetch tool, so `c-dk-critique-noise` + `ev-dk-critique-noise` stay `abstract_only`, `publishable:false`. That is the citation/queue layer, not garbage: a resolvable DOI with a pending full-text read, no fabricated body quote.
- Dunning-Kruger now deliberately spans layers: one published popular-framing claim, three unpublished (research finding, Gignac critique, Nuhfer noise critique) awaiting readable full text. All other P2-E claims remain `metadata_only`, `publishable:false`. The validator's gate is now actually exercised (one claim through it) rather than merely intact.

## P1 progress

- `named-effects-routing-pilot` is the second named-phenomenon slice: a deliberately bounded two-item `discovery_seed` pairing chosen by PLAN P2-E to test evidence routing across different evidence types. It registers `misattribution-of-arousal` (吊橋效應, Dutton–Aron bridge experiment; a lab social-psychology emotion effect) and `broken-windows-effect` (破窗效應, Wilson & Kelling 1982; a contested field criminology/social-order effect). Both are `included` identity-only, `publishable:false`. With the already-registered Dunning–Kruger effect, all three P2-E routing pilots now have identities. The broken-windows note explicitly records that the effect is contested, so identity registration cannot be mistaken for validity.
- `wikipedia-cognitive-biases-core` is the first named-phenomenon slice and the first `discovery_seed`. It registers 23 widely taught cognitive biases (confirmation bias, anchoring, availability/representativeness heuristics, Dunning–Kruger, framing, halo, fundamental attribution error, loss aversion, etc.) as `phenomenon` entities with a controlled `phenomenon_kind`, a resolvable `domain_entity_ids` host, and a Chinese label. All 23 are `included`; there are no merges because no prior entity represented a phenomenon. This is deliberately bounded: the source page has ~210 loosely structured entries, so `complete:true` means every declared candidate is adjudicated, not that the cognitive-bias universe is exhausted. A discovery seed can only produce candidates; it cannot support an evidence verdict, and every record stays `publishable:false`.
- `apa-coa-postdoctoral-specialty-practice-areas` is the first completed reference-system slice: 11/11 official candidates are recorded and mapped to non-publishable `subfield` identities.
- Its scope is deliberately narrow: United States health-service psychology postdoctoral specialty accreditation. It is not evidence for a global or exhaustive psychology taxonomy.
- `anzsrc-2020-for-psychology-groups` is the second completed slice: 6/6 group-level candidates under Division 52 are adjudicated. Five substantive groups are included; residual code 5299 `Other psychology` is recorded but excluded as a non-coherent entity.
- ANZSRC is an Australia/New Zealand R&D classification, not a global ontology. Its Division 52 explicitly sends Indigenous psychology to Division 45 Indigenous studies, so the atlas must inspect that axis rather than treating the omission as absence.
- Similar labels remain distinct when their scopes differ: ANZSRC `Clinical and health psychology` is not merged into the narrower APA CoA `Clinical Health Psychology` specialty.
- `anzsrc-2020-for-psychology-fields` registers and resolves all 36 Division 52 field codes. The 5201 batch has 7 included fields, 1 identity merge (`Forensic psychology`), and 1 NEC residual excluded. The 5202 batch has 7 substantive biological-psychology fields included. The 5203 batch has 3 included fields, 1 identity merge (`Clinical neuropsychology`), and a preserved boundary between ANZSRC `Health psychology` and the narrower APA CoA `Clinical Health Psychology` specialty. The 5204 batch preserves all 6 entries as research-field identities, including compound statistical labels, without converting them into construct claims. The 5205 batch includes 5 research fields while preserving compound-label, adjacent-discipline, and cross-project boundaries. Final field totals are 28 included, 2 merged, 6 excluded, and 0 pending.
- `iaap-active-divisions` is the first global organizational slice: all 18 active IAAP divisions are registered and resolved from the official live page. Its scope is explicitly global applied psychology and membership organization, not an exhaustive psychology taxonomy. Twelve substantive or compound applied fields are included; Work and Organizational Psychology, Health Psychology, Sport Psychology, and Counseling Psychology merge into existing cross-system identities while preserving source scope; the student/early-career cohort and cross-cutting Professional Practice function are excluded. Final totals are 12 included, 4 merged, 2 excluded, and 0 pending.
- `anzsrc-2020-for-indigenous-studies-groups` registers and resolves all 20 group-level codes under Division 45 as a contextual Indigenous axis. It preserves separate Aboriginal and Torres Strait Islander, Māori, Pacific Peoples, and global Indigenous data/methodologies structures rather than selecting only health or society categories. A new `context_domain` entity type prevents these broad fields from masquerading as psychology subfields. Groups 4501–4506 are included as Aboriginal and Torres Strait Islander context domains; groups 4507–4512 are included as Māori context domains with te reo Māori canonical names and English aliases; groups 4513–4518 are included as Pacific Peoples context domains; group 4519 preserves global Indigenous data, technologies, methodologies and source-specific exclusions. Groups 4504, 4510 and 4516 are directly psychology-relevant because their official definitions explicitly include psychological wellbeing. The corrected ABS cube assigns 4517 to society and community and 4518 to sciences. Final totals are 19 included context domains, 1 excluded residual, and 0 pending.
- Coverage reports now separate `complete` (every source candidate has a record) from `resolved` (no pending decisions). The field inventory is `complete:true`, `resolved:false`; this prevents a full candidate scrape from masquerading as completed adjudication.
- Coverage completeness is now executable: every declared candidate must have exactly one `included`, `merged`, `excluded`, or `pending` decision, and included/merged targets must resolve.
- Generated `views/generated/coverage-report.json` is disposable and reproducible from canonical records.

## APPROVED FUTURE WORK（QUEUED, NOT ACTIVE）

- P1-E：建立命名效應／偏誤／現象的 schema 與 bounded candidate universe；名稱不等於證據。
- P2-E：建立來源庫與證據路由，先以吊橋效應、達克效應、破窗效應測試不同證據型態。
- P3-M：建立 physical → chemical / biological → cognitive / behavioral → social / cultural 的受控機制層級，並先驗證 relationship evidence linkage。
- P3-M 首個建議 pilot：光照、晝夜節律／褪黑激素、睡眠、認知情緒、行為與社會作息的跨層鏈。
- P4-E/M：產生 Named Effect Card、Popular Claim vs Evidence、Replication / Controversy 與 Mechanism Ladder 視圖。
- 啟動條件：必須先完成 `ACTIVE WORK` 的 `next_gate`；排入 roadmap 不代表可提前建立 claims。

## Legacy provenance

- 舊 repo：`C:\claudehome\projects\psychology-schools`
- 舊正式 checkpoint：`master@3be7f99`（建立新版時）
- 舊完整 WIP：branch `archival/wip-atlas-migration-2026-07-22`、commit `eb115a5`
- 舊 §3a 本土心理學改動未匯入；Axline 修正已在舊 master 獨立保存。

## 發布狀態

`evidence_release: false`（atlas 層仍未發布）。已有兩筆通過閘門的 `publishable:true` claim：`c-dk-popular`（達克效應的通俗說法，非「效應為真」主張）與 `c-anchoring-manylabs-replication`（第一筆 research 層 finding，錨定效應在 Many Labs 1 多實驗室複製中屬「非常大的效應」，讀自開放全文）。其餘 claim 落在誠實引用／待辦層或候選層。個別 claim 可 publishable 不等於整個 atlas 進入 evidence_release。
