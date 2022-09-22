import 'package:flutter/cupertino.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:mobile_cafe/utils/colors.dart';

class BigText extends StatelessWidget {
  final Color? color;
  final String text;
  final double size;
  final TextOverflow overFlow;
  const BigText(
      {super.key,
      this.color = const Color(0xFF332d2b),
      required this.text,
      this.size = 20,
      this.overFlow = TextOverflow.ellipsis});

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      maxLines: 1,
      overflow: overFlow,
      style: TextStyle(
          fontFamily: 'Roboto',
          color: color,
          fontWeight: FontWeight.w400,
          fontSize: size),
    );
  }
}
