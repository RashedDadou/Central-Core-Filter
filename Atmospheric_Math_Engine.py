class Atmospheric_Math_Engine:
    """المحرك الرياضي الثاني: يحسب احتكاك المادة بكتلة الهواء والضغط لتوليد الوزن والتسارع والارتطام"""
    def __init__(self, air_density=1.225):
        # الكثافة المرجعية للهواء عند سطح الأرض (كيلوجرام / متر مكعب)
        # يمكن تعديلها لمحاكاة منخفض جوي (مثلاً 1.0) أو مرتفع جوي (مثلاً 1.4)
        self.rho = float(air_density) 

    def Calculate_Atmospheric_Forces(self, body_mass, surface_area, current_velocity, g_pull, current_height=7000.0, material_type="stone"):
        """
        [تطوير مضرّس - رؤية المعماري راشد]: حساب الضغط الشطيري للهواء المتكدس (دفع من الأعلى + فرملة من الأسفل)
        ينتج عنها: السرعة الحقيقية، الوزن المشهدي، وقوة الارتطام المتوقعة.
        """
        v = abs(current_velocity)
        
        # 1. حساب ميكانيكية تكدس جزيئات الهواء بفعل الارتفاع (من 7 كم نزولاً إلى الصفر)
        reference_height = 7000.0
        clamped_height = min(max(current_height, 0.0), reference_height)
        # الكثافة الفعلية تزداد كلما هبطنا لأسفل واقتربنا من الأرض
        actual_rho = self.rho * (1.0 + (1.0 - (clamped_height / reference_height)))

        # 2. العامل الأول [من الأسفل]: قوة الاحتكاك والفرملة بجزيئات الهواء المتكدسة (تتجه للأعلى)
        f_resistance = 0.5 * actual_rho * surface_area * (v ** 2)
        
        # 3. حساب قوة السحب الأساسية (الكتلة x سحب الجاذبية الموحد الصامت)
        f_pull = body_mass * g_pull
        
        # 4. العامل الثاني [من الأعلى]: قوة الدفع والتدافع لأسفل الناجمة عن وزن عامود الهواء المتكدس فوق المادة
        # الحجر كمادة صلبة ومصمتة يستقبل كامل طاقة هذا الثقل العمودي لأسفل
        if material_type == "stone":
            f_downforce_air = actual_rho * surface_area * g_pull * 2.5 # دفع مفرط لأسفل بسبب طبيعة المادة الصلبة
        else:
            f_downforce_air = actual_rho * surface_area * g_pull * 0.2 # دفع ضئيل للمواد الخفيفة كالريشة

        # 5. [المعرفة الشطيرية]: الوزن الصافي للمشهد الناتج عن (السحب الثابت + دفع الهواء لأسفل) - (الفرملة من الأسفل)
        f_net = (f_pull + f_downforce_air) - f_resistance
        
        # 6. حساب التسارع الحقيقي المتغير في الجو بفعل تلاحم القوى
        true_acceleration = f_net / body_mass
        
        return true_acceleration, f_net

    def Calculate_Impact_Energy(self, body_mass, final_velocity):
        """حساب طاقة الارتطام الناتجة عن اصطدام الكتلة بالأرض بناءً على سرعتها النهائية"""
        # طاقة الحركة لحظة الاصطدام بالجول (Joule)
        impact_energy = 0.5 * body_mass * (final_velocity ** 2)
        return impact_energy