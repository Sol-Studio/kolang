import re, sys, os, getopt
__version = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.txt"), "r", encoding="utf-8").read()


class RePreset:
    """
    변환에 사용되는 정규식의 모음
    """
    function = r"(.+)(해|와|아)라"
    assign = r"(.+) => (.+)"
    param = r"(.+)(을 |를 )"
    condition_if = r"만약 (.+)(이|가) (.+)(보다|과|와) (작거나 같다|크거나 같다|작다|크다|같다|다르다)면"
    repeat = r"(.+) 반복해라"
    list_index = r".+의 [1-9\[\]:]+번째 요소들?"
    of_instance = r"(.+)(의|에) (.+)"
    define_func = r"함수 이름:([^ ]+)(, 매개변수:(.+))?(을|를) 정의하겠다"
    use_extension = r"확장기능 (.+)(을|를) 사용하겠다"


# 코랭 - python
funcDB = {
    # 기본
    "출력":"print",
    "입력받": "input",
    "계산": "eval",
    "불러": "__import__",
    "정수로변환": "int",
    "문자로변환": "str",
    "종료": "exit",

    # 기본기능
    "저장": "kolang.ext.default.save", 
    "화면청소": "kolang.ext.default.cls",

    # gui 확장기능
    "gui.창.이름변경": "kolang.ext.gui.change_window_title",
    "gui.창생성": "kolang.ext.gui.create_window",
    "gui.창.크기위치수정": "kolang.ext.gui.set_window_geometry",
    "gui.요소.텍스트수정": "kolang.ext.gui.edit_label",
    "gui.요소추가": "kolang.ext.gui.create_component",
    "gui.요소삭제": "kolang.ext.gui.delete_component",

    # time 확장기능
    "시간.기다리기": "kolang.ext.time.sleep",
    "시간.지금시간구하기": "kolang.ext.time.getTimeString"
}
keywordDB = {
    "계속": "continue",
    "멈춰": "break",
    "지나가": "pass",
    "반환해": "return",
    "전역변수": "global"
}
extDB = {
    "gui": "gui",
    "시간": "time"
}


def convertLn(string:str) -> str:
    """
    한 줄의 sol코드를 파이썬 코드로 변환하여 반환합니다.
    string : 변환할 한 줄의 코드
    """

    compiled = ""
    funcName = ""
    param = ""
    tab_stack = 0

    # 탭 (\t)가 몇번 들어있는지 확인
    while string.startswith("    "):
        string = string[4:]
        tab_stack += 1

    # 주석 처리
    if string.startswith("#"):
        return tab_stack*"\t" + string

    # 빈 줄인지 확인
    if string == "":
        return tab_stack*"\t"

    # 키워드 (break, continue, ..)
    if string.split(" ")[0] in keywordDB.keys():
        return tab_stack*"    " + keywordDB[string.split(" ")[0]] + " " + " ".join(string.split(" ")[1:])


    # 할당
    assign = re.search(RePreset.assign, string)
    if assign != None:
        compiled = assign.groups()[1] + " = "
        string = assign.groups()[0]

    # 확장
    use_extension = re.fullmatch(RePreset.use_extension, string)
    if use_extension != None:
        ext = use_extension.group(1)
        if ext not in extDB.keys():
            raise NameError("확장기능 " + ext + "(는)은 존재하지 않습니다")
        return "    "*tab_stack + "import kolang.ext." + extDB[ext]


    # 조건문
    condition = re.fullmatch(RePreset.condition_if, string)
    if condition != None:
        condition = condition.groups()
        if condition[3]== "보다":
            compiled = "if " + condition[0] + {"작거나같다":" <= ", "크거나같다":" >= ", "작다":" < ", "크다":" > "}[condition[4]] + condition[2] + ":"

        else:
            compiled = "if " + condition[0] + {"같다": " == ", "다르다":" != "}[condition[4]] + condition[2] + ":"

        return "    "*tab_stack + compiled

    # 반복문
    repeat = re.fullmatch(RePreset.repeat, string)
    if repeat != None:
        repeat = repeat.groups()
        if repeat[0][-1] == "번":
            if repeat[0][:2] == "무한":
                return "\t"*tab_stack + "while True:"

            else:
                return "\t"*tab_stack + "for i in range(" + repeat[0][:-1] + "):"
        else:
            return "\t"*tab_stack + "for i in " + repeat[0] + ":"

    # 함수 정의
    define_func = re.fullmatch(RePreset.define_func, string)
    if define_func != None:
        return "    "*tab_stack + "def " + define_func.group(1) + "(" + (lambda s: s if (s is not None) else "")(define_func.group(3)) + "):"

    # 함수
    funcMatch = re.search(RePreset.function, string)
    if funcMatch:
        funcName = funcMatch.groups()[0].split(" ")[-1]
        if funcName in funcDB.keys():
            funcName = funcDB[funcName]


        # 파라미터
        paramString = ""
        paramMatch = re.search(RePreset.param, string)
        if paramMatch != None:
            paramString = paramMatch.groups()[0]


        # 함수 완성
        func = funcName + "(" + paramString + ")"
        compiled += func


    return "    "*tab_stack + compiled


def convertFile(inFilePath:str, outFileDir:str) -> str:
    """
    .sol 파일을 파이썬 파일로 변환하고 그 경로를 반환합니다.
    inFilePath : 변환할 파일의 경로
    """
    # inFilePath이 존재하지 않으면 오류 발생
    if not os.path.exists(inFilePath):
        raise FileNotFoundError("파일 \"%s\"가 존재하지 않습니다" % inFilePath)

    # outFileDir이 존재하지 않으면 만들기
    if not os.path.exists(outFileDir):
        os.makedirs(outFileDir, exist_ok=True)

    # 코랭 코드 불러오기
    strings = open(inFilePath, "r", encoding="utf-8").read().split("\n")

    converted = ""
    for s in strings:
        converted += convertLn(s) + "\n"
    outFilePath = os.path.join(outFileDir, inFilePath.split(".")[-1] + ".py")
    open(outFilePath, "w", encoding="utf-8").write("import kolang\n"+converted)
    return outFilePath


# 콘솔 명령어 처리
def main():
    if len(sys.argv) < 2:
        print("안녕하세요! 코랭이에요!")
        return
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vho:", ["version", "help", "output="])
        
    except getopt.GetoptError as err:
        print("알맞지 않은 옵션 형식입니다. 도움말을 보려면 \"kolang --help\"를 입력하세요")
        return
    
    inFilePath = ""
    outFileDir = "dist"
    
    for opt,arg in opts:
        if opt == "-o" or opt == "--output":
            outFileDir = arg

        elif opt == "-v" or opt == "--version":
            print("코랭 버전 : %s\n파이썬 버전 : %d.%d.%d" % (__version, sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
            return

        elif opt == "-h" or opt == "--help":
            print("""
    kolang [run|convert] [파일경로] -o(선택사항) [변환된 파일이 저장될 폴더(default:/.dist)] : 코랭 코드를 실행하거나 파이썬 파일로 변환합니다
    kolang --help(-h) : 도움말
    kolang --version(-v) : 코랭과 파이썬의 버전을 확인합니다
            """)
            return

        else:
            print(opt + "은(는) 알 수 없는 옵션입니다. 도움말을 보려면 \"kolang --help\"를 입력하세요")


    command = sys.argv[1]
    if command == "run":
        if len(sys.argv) < 3:
            print("변환할 파일 옵션이 빠져있습니다. 도움말을 보려면 \"kolang --help\"를 입력하세요")
            return
        inFilePath = sys.argv[2]
        os.system("python " + convertFile(inFilePath, outFileDir))


    elif command == "convert":
        if len(sys.argv) < 3:
            print("변환할 파일 옵션이 빠져있습니다. 도움말을 보려면 \"kolang --help\"를 입력하세요")
            return
        inFilePath = sys.argv[2]
        convertFile(inFilePath, outFileDir)
        print("코랭 코드 '%s'를 '%s'로 변환하였습니다." % (sys.argv[2], filename))


    else:
        print(command + "은(는) 알 수 없는 명령어입니다. 도움말을 보려면 \"kolang --help\"를 입력하세요")


if __name__ == "__main__":
    main()